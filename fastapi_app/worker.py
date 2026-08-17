import os
import sys
import time
import asyncio
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

# App imports
from models import SessionLocal, Project, DatabaseNode, SyncJob, AuditLog
from ha_manager import setup_replication

WORKER_ID = os.environ.get("RENDER_INSTANCE_ID", f"local-{os.getpid()}")
POLL_INTERVAL = 5
LEASE_TIMEOUT_SECONDS = 60

async def process_job(db: Session, job: SyncJob):
    project_id = job.project_id
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        job.status = "FAILED"
        job.error_message = "Project not found"
        db.commit()
        return

    async def update_status(status: str):
        job.status = status
        db.commit()

    try:
        await update_status("VALIDATING")
        primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
        standbys = [n for n in proj.nodes if n.role.lower() == 'standby']
        
        if not primary or not standbys:
            raise Exception("Project must have at least 1 Primary and 1 Standby node.")
            
        standbys_info = [{"id": s.id, "url": s.encrypted_url} for s in standbys]
        
        result = await setup_replication(project_id, primary.encrypted_url, standbys_info, proj.replication_tables, update_status)
        
        if result['success']:
            job.status = "SUCCESS"
            job.error_message = None
            proj.replication_health = "HEALTHY"
            
            audit = AuditLog(project_id=project_id, action="Replication Synced", details="Background Sync Job completed successfully.")
            db.add(audit)
        else:
            job.status = "FAILED"
            job.error_message = result.get('message', 'Unknown Error')
            proj.replication_health = "FAILED"
            
            audit = AuditLog(project_id=project_id, action="Sync Failed", details=job.error_message)
            db.add(audit)
            
    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        proj.replication_health = "FAILED"
        
    finally:
        job.completed_at = datetime.datetime.utcnow()
        job.lease_owner = None
        db.commit()

def fetch_and_lock_job(db: Session) -> SyncJob:
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(seconds=LEASE_TIMEOUT_SECONDS)
    
    # Atomic CTE query: Finds the row, locks it, updates status & lease, and returns the ID
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
            lease_expires_at = :expires_at
        WHERE id = (SELECT id FROM locked_job)
        RETURNING id;
    """)
    result = db.execute(query, {"now": now, "worker_id": WORKER_ID, "expires_at": expires}).fetchone()
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
            job = fetch_and_lock_job(db)
            if job:
                print(f"Worker [{WORKER_ID}] picked up Job ID: {job.id} for Project ID: {job.project_id}")
                
                async def heartbeat():
                    while True:
                        await asyncio.sleep(LEASE_TIMEOUT_SECONDS / 3)
                        hb_db = SessionLocal()
                        try:
                            # Conditional update ensures we don't blindly renew if lease was lost
                            res = hb_db.execute(
                                text("UPDATE sync_jobs SET lease_expires_at = :expires WHERE id = :job_id AND lease_owner = :worker_id AND status NOT IN ('SUCCESS', 'FAILED')"),
                                {"expires": datetime.datetime.utcnow() + datetime.timedelta(seconds=LEASE_TIMEOUT_SECONDS), "job_id": job.id, "worker_id": WORKER_ID}
                            )
                            hb_db.commit()
                            # If rowcount is 0, we lost the lease or job finished
                            if res.rowcount == 0:
                                break
                        except Exception as hb_err:
                            print(f"Heartbeat error: {hb_err}")
                        finally:
                            hb_db.close()
                            
                heartbeat_task = asyncio.create_task(heartbeat())
                
                try:
                    await process_job(db, job)
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
            db.close()

if __name__ == "__main__":
    asyncio.run(main_loop())
