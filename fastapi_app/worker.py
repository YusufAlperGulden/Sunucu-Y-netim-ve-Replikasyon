import os
import sys
import time
import asyncio
import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text

# App imports
from models import SessionLocal, Project, DatabaseNode, SyncJob, AuditLog
from ha_manager import setup_replication

WORKER_ID = os.environ.get("RENDER_INSTANCE_ID", f"local-{os.getpid()}")
POLL_INTERVAL = 5
LEASE_TIMEOUT_SECONDS = 60

async def process_job(db: Session, job: SyncJob, worker_id: str, lease_lost_event: asyncio.Event):
    project_id = job.project_id
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        # Note: If lease is lost, this might overwrite someone else's state if we don't fence
        job.status = "FAILED"
        job.error_message = "Project not found"
        db.commit()
        return

    # Create a helper function to safely update status with fencing token
    def execute_fenced_update(status_to_set=None, error_msg=None, complete=False):
        update_cols = []
        params = {"job_id": job.id, "worker_id": worker_id, "token": job.lease_token}
        
        if status_to_set:
            update_cols.append("status = :status")
            params["status"] = status_to_set
            
        if error_msg is not None:
            update_cols.append("error_message = :error_msg")
            params["error_msg"] = error_msg
            
        if complete:
            update_cols.append("completed_at = :now, lease_owner = NULL, lease_token = NULL")
            params["now"] = datetime.datetime.utcnow()
            
        if not update_cols:
            return True
            
        set_clause = ", ".join(update_cols)
        query = text(f"""
            UPDATE sync_jobs 
            SET {set_clause}
            WHERE id = :job_id AND lease_owner = :worker_id AND lease_token = :token
        """)
        
        res = db.execute(query, params)
        db.commit()
        return res.rowcount > 0

    async def update_status(status: str):
        if not execute_fenced_update(status_to_set=status):
            raise Exception("Lease lost during status update")

    try:
        await update_status("VALIDATING")
        primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
        standbys = [n for n in proj.nodes if n.role.lower() == 'standby']
        
        if not primary or not standbys:
            raise Exception("Project must have at least 1 Primary and 1 Standby node.")
            
        standbys_info = [{"id": s.id, "url": s.encrypted_url} for s in standbys]
        
        # We pass a callback to ha_manager that checks if this task was cancelled or lease lost event is set
        def check_lease():
            if lease_lost_event.is_set():
                raise RuntimeError("Task cancelled due to lease loss")
            
        result = await setup_replication(project_id, primary.encrypted_url, standbys_info, proj.replication_tables, update_status, check_lease_cb=check_lease)
        
        if result['success']:
            if execute_fenced_update(status_to_set="SUCCESS", error_msg=None, complete=True):
                proj.replication_health = "HEALTHY"
                audit = AuditLog(project_id=project_id, action="Replication Synced", details="Background Sync Job completed successfully.")
                db.add(audit)
                db.commit()
        else:
            if execute_fenced_update(status_to_set="FAILED", error_msg=result.get('message', 'Unknown Error'), complete=True):
                proj.replication_health = "FAILED"
                audit = AuditLog(project_id=project_id, action="Sync Failed", details=result.get('message', 'Unknown Error'))
                db.add(audit)
                db.commit()
            
    except Exception as e:
        if execute_fenced_update(status_to_set="FAILED", error_msg=str(e), complete=True):
            proj.replication_health = "FAILED"
            db.commit()

def fetch_and_lock_job(db: Session, worker_id: str) -> SyncJob:
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(seconds=LEASE_TIMEOUT_SECONDS)
    token = str(uuid.uuid4())
    
    # Atomic CTE query: Finds the row, locks it, updates status, lease owner, and token
    query = text("""
        WITH locked_job AS (
            SELECT id FROM sync_jobs 
            WHERE status = 'QUEUED' 
               OR (status IN ('VALIDATING', 'BOOTSTRAPPING', 'CATCHING_UP', 'RECOVERING') AND lease_expires_at < :now)
            ORDER BY created_at ASC 
            LIMIT 1 
            FOR UPDATE SKIP LOCKED
        )
        UPDATE sync_jobs 
        SET status = CASE WHEN status = 'QUEUED' THEN 'VALIDATING' ELSE 'RECOVERING' END,
            lease_owner = :worker_id,
            lease_token = :token,
            lease_expires_at = :expires_at
        WHERE id = (SELECT id FROM locked_job)
        RETURNING id;
    """)
    result = db.execute(query, {"now": now, "worker_id": worker_id, "token": token, "expires_at": expires}).fetchone()
    db.commit()
    
    if not result:
        return None
        
    job_id = result[0]
    return db.query(SyncJob).filter(SyncJob.id == job_id).first()

async def main_loop():
    print(f"Starting Background Worker [{WORKER_ID}]...")
    while True:
        db = SessionLocal()
        try:
            job = fetch_and_lock_job(db, WORKER_ID)
            if job:
                print(f"Worker [{WORKER_ID}] picked up Job ID: {job.id} for Project ID: {job.project_id}")
                
                lease_lost_event = asyncio.Event()
                
                # Make the process task aware of lease loss event
                async def process_job_wrapper():
                    try:
                        await process_job(db, job, WORKER_ID, lease_lost_event)
                    except asyncio.CancelledError:
                        lease_lost_event.set()
                        raise
                        
                process_task = asyncio.create_task(process_job_wrapper())

                async def heartbeat():
                    import time
                    lease_deadline = time.monotonic() + LEASE_TIMEOUT_SECONDS
                    safe_margin = 10.0 # seconds
                    
                    while True:
                        await asyncio.sleep(5)
                        if process_task.done():
                            break
                            
                        if time.monotonic() > (lease_deadline - safe_margin):
                            print(f"Worker [{WORKER_ID}] lease about to expire locally. Cancelling task for safety.")
                            lease_lost_event.set()
                            process_task.cancel()
                            break

                        try:
                            def update_heartbeat():
                                with SessionLocal() as hb_db:
                                    res = hb_db.execute(
                                        text("UPDATE sync_jobs SET lease_expires_at = :expires WHERE id = :job_id AND lease_owner = :worker_id AND lease_token = :token AND status NOT IN ('SUCCESS', 'FAILED')"),
                                        {"expires": datetime.datetime.utcnow() + datetime.timedelta(seconds=LEASE_TIMEOUT_SECONDS), "job_id": job.id, "worker_id": WORKER_ID, "token": job.lease_token}
                                    )
                                    hb_db.commit()
                                    return res.rowcount
                            
                            rowcount = await asyncio.to_thread(update_heartbeat)
                            if rowcount == 0:
                                print(f"Worker [{WORKER_ID}] lost lease for Job ID: {job.id}")
                                lease_lost_event.set()
                                process_task.cancel()
                                break
                            else:
                                lease_deadline = time.monotonic() + LEASE_TIMEOUT_SECONDS
                        except Exception as hb_err:
                            print(f"Heartbeat error: {hb_err}")
                            
                heartbeat_task = asyncio.create_task(heartbeat())
                
                try:
                    await process_task
                except asyncio.CancelledError:
                    print(f"Worker [{WORKER_ID}] job processing cancelled due to lease loss.")
                finally:
                    heartbeat_task.cancel()
                    # Wait for the task to actually cancel
                    try:
                        await heartbeat_task
                    except asyncio.CancelledError:
                        pass
            else:
                await asyncio.sleep(POLL_INTERVAL)
        except Exception as e:
            print(f"Worker error: {e}")
            await asyncio.sleep(POLL_INTERVAL)
        finally:
            
        # --- Handle Backup Jobs ---
        from models import BackupJob
        from datetime import datetime
        import random
        
        pending_backups = db.query(BackupJob).filter(BackupJob.status == "IN_PROGRESS").all()
        for job in pending_backups:
            # Simulate a 10-20 second backup time
            diff = (datetime.utcnow() - job.created_at).total_seconds()
            if diff > random.randint(15, 30):
                job.status = "COMPLETED"
                job.size_mb = round(random.uniform(500.0, 5000.0), 2)
                job.completed_at = datetime.utcnow()
                db.commit()
                print(f"Simulated backup {job.id} completed.")

        db.close()

if __name__ == "__main__":
    asyncio.run(main_loop())
