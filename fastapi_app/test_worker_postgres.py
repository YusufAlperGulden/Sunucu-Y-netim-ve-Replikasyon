import os
import sys
import threading
import time
import datetime
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def main():
    TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
    if not TEST_DATABASE_URL:
        print("TEST_EXIT_CODE=1")
        print("ERROR: TEST_DATABASE_URL environment variable is required.")
        sys.exit(1)
        
    allow_destructive = os.environ.get("ALLOW_DESTRUCTIVE_TESTS")
    if allow_destructive != "1":
        print("TEST_EXIT_CODE=1")
        print("ERROR: ALLOW_DESTRUCTIVE_TESTS=1 is required to drop and create tables.")
        sys.exit(1)

    # 1. Güvenlik kontrollerinden sonra uygulamanın geri kalanını yükle
    if TEST_DATABASE_URL.startswith("postgres://"):
        TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    # Ensure VAULT_KEY is available to load models which load vault
    if not os.environ.get("VAULT_KEY"):
        os.environ["VAULT_KEY"] = "M3YtdrYQO8q-1XW085s5Xw16_P_hV58N0d2R0S-q0sY=" # dummy key for test
        
    import models
    import worker
    from models import Base, SyncJob, Project

    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def setup_data():
        db = SessionLocal()
        p = Project(name="Test Project")
        db.add(p)
        db.commit()
        proj_id = p.id
        j = SyncJob(project_id=proj_id, status="QUEUED")
        db.add(j)
        db.commit()
        db.close()
        return proj_id

    barrier = threading.Barrier(2)
    test_results = {"worker_1": None, "worker_2": None}
    exceptions = []

    def run_worker(worker_id):
        try:
            db = SessionLocal()
            worker.SessionLocal = SessionLocal
            
            barrier.wait()
            
            job = None
            try:
                job = worker.fetch_and_lock_job(db, worker_id)
                if job:
                    print(f"Worker {worker_id} successfully claimed job {job.id}")
                    test_results[worker_id] = "CLAIMED"
                    
                    # Mock processing block
                    def update_status():
                        pass
                        
                    time.sleep(1)
                    
                    # We can't use await here because this is a synchronous threading block
                    # For testing just the locking/claiming we don't need the async process_job
                    # We just use the fenced update directly
                    query = text("""
                        UPDATE sync_jobs 
                        SET status = 'SUCCESS', completed_at = :now, lease_owner = NULL, lease_token = NULL
                        WHERE id = :job_id AND lease_owner = :worker_id AND lease_token = :token
                    """)
                    res = db.execute(query, {"job_id": job.id, "worker_id": worker_id, "token": job.lease_token, "now": datetime.datetime.utcnow()})
                    db.commit()
                    if res.rowcount == 0:
                        raise Exception("Failed to commit final status, lease was lost.")
                else:
                    print(f"Worker {worker_id} found no jobs to claim")
                    test_results[worker_id] = "MISSED"
            finally:
                db.close()
        except Exception as e:
            print(f"Thread {worker_id} crashed: {e}")
            exceptions.append(e)

    def test_concurrent_claim():
        proj_id = setup_data()
        
        print("Starting concurrent workers with threading barrier...")
        t1 = threading.Thread(target=run_worker, args=("worker_1",))
        t2 = threading.Thread(target=run_worker, args=("worker_2",))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        if exceptions:
            print(f"TEST FAILED: {len(exceptions)} exceptions occurred during threads.")
            sys.exit(1)
            
        print(f"Results: worker_1 -> {test_results['worker_1']}, worker_2 -> {test_results['worker_2']}")
        assert (test_results["worker_1"] == "CLAIMED" and test_results["worker_2"] == "MISSED") or (test_results["worker_1"] == "MISSED" and test_results["worker_2"] == "CLAIMED")
        
        db = SessionLocal()
        final_job = db.query(SyncJob).filter(SyncJob.project_id == proj_id).first()
        print(f"Final Job Status: {final_job.status}, completed at {final_job.completed_at}, owner: {final_job.lease_owner}")
        assert final_job.status == "SUCCESS"
        assert final_job.lease_owner is None
        assert final_job.lease_token is None
        
        print("TEST_EXIT_CODE=0")
        db.close()

    test_concurrent_claim()

if __name__ == "__main__":
    from sqlalchemy import text
    main()
