import re

worker_path = 'fastapi_app/worker.py'
with open(worker_path, 'r', encoding='utf-8') as f:
    content = f.read()

backup_worker = """
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
"""

if "BackupJob" not in content:
    # insert before db.close() inside the loop
    content = content.replace("db.close()", backup_worker + "\n        db.close()")
    with open(worker_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added backup worker logic")
