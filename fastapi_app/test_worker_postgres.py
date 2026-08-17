import os
import sys
import threading
import time
import datetime
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
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
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

    # Bariyer: İşçilerin tam olarak aynı anda `fetch_and_lock_job` çağırmasını sağlamak için
    barrier = threading.Barrier(2)

    def run_worker(worker_id):
        # Her thread kendi veritabanı oturumunu kullanır
        db = SessionLocal()
        
        # Module global değişkenlerini patchle
        worker.WORKER_ID = worker_id
        worker.SessionLocal = SessionLocal
        
        barrier.wait() # İki thread'in de buraya gelmesini bekle
        
        job = None
        try:
            job = worker.fetch_and_lock_job(db)
            if job:
                print(f"Worker {worker_id} successfully claimed job {job.id}")
                # Mock processing
                time.sleep(1)
                job.status = "SUCCESS"
            else:
                print(f"Worker {worker_id} found no jobs to claim (likely locked by another worker)")
        finally:
            if job:
                job.completed_at = datetime.datetime.utcnow()
                job.lease_owner = None
                db.commit()
            db.close()

    def test_concurrent_claim():
        proj_id = setup_data()
        
        print("Starting concurrent workers with threading barrier...")
        t1 = threading.Thread(target=run_worker, args=("worker_1",))
        t2 = threading.Thread(target=run_worker, args=("worker_2",))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        db = SessionLocal()
        final_job = db.query(SyncJob).filter(SyncJob.project_id == proj_id).first()
        print(f"Final Job Status: {final_job.status}, completed at {final_job.completed_at}, owner: {final_job.lease_owner}")
        assert final_job.status == "SUCCESS"
        assert final_job.lease_owner is None
        print("TEST_EXIT_CODE=0")
        db.close()

    test_concurrent_claim()

if __name__ == "__main__":
    main()
