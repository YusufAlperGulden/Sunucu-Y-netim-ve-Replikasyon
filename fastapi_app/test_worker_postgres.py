import os
import sys
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

import models
import worker
from models import Base, SyncJob, Project

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
        
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def setup_data():
        db = SessionLocal()
        p = Project(name="Test Project")
        db.add(p)
        db.commit()
        return p.id

    async def mock_process_job(db, job):
        await asyncio.sleep(2) # simulate work
        job.status = "SUCCESS"
        db.commit()

    async def run_worker(worker_id):
        db = SessionLocal()
        
        # Patch module variables for this worker execution
        worker.WORKER_ID = worker_id
        worker.SessionLocal = SessionLocal
        
        job = None
        try:
            job = worker.fetch_and_lock_job(db)
            if job:
                print(f"Worker {worker_id} successfully claimed job {job.id}")
                await mock_process_job(db, job)
            else:
                print(f"Worker {worker_id} found no jobs to claim (likely locked by another worker)")
        finally:
            if job:
                job.completed_at = datetime.datetime.utcnow()
                job.lease_owner = None
                db.commit()
            db.close()

    async def test_concurrent_claim():
        proj_id = setup_data()
        db = SessionLocal()
        j = SyncJob(project_id=proj_id, status="QUEUED")
        db.add(j)
        db.commit()
        db.close()
        
        print("Starting concurrent workers...")
        await asyncio.gather(
            run_worker("worker_1"),
            run_worker("worker_2")
        )
        
        db = SessionLocal()
        final_job = db.query(SyncJob).filter(SyncJob.project_id == proj_id).first()
        print(f"Final Job Status: {final_job.status}, completed at {final_job.completed_at}, owner: {final_job.lease_owner}")
        assert final_job.status == "SUCCESS"
        assert final_job.lease_owner is None
        print("TEST_EXIT_CODE=0")
        
    asyncio.run(test_concurrent_claim())

if __name__ == "__main__":
    main()
