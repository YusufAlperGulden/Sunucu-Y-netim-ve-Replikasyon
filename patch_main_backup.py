import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

backup_apis = """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BackupCreate(BaseModel):
    project_id: int
    backup_type: str

@app.post("/api/backups", dependencies=[Depends(verify_credentials)])
def create_backup(payload: BackupCreate, db: Session = Depends(get_db)):
    from models import BackupJob
    proj = db.query(Project).filter(Project.id == payload.project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    job = BackupJob(
        project_id=proj.id,
        cluster_name=proj.name,
        backup_type=payload.backup_type,
        status="IN_PROGRESS"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # In a real scenario, we'd fire an async background task here.
    # For now, we simulate completion after a short delay via worker.
    from models import AuditLog
    audit = AuditLog(project_id=proj.id, action="Backup Initiated", details=f"Type: {payload.backup_type}")
    db.add(audit)
    db.commit()
    
    return {"success": True, "job_id": job.id, "message": "Backup started successfully"}

@app.get("/api/backups", dependencies=[Depends(verify_credentials)])
def get_backups(db: Session = Depends(get_db)):
    from models import BackupJob
    jobs = db.query(BackupJob).order_by(BackupJob.id.desc()).all()
    results = []
    for j in jobs:
        results.append({
            "id": j.id,
            "project_id": j.project_id,
            "cluster_name": j.cluster_name,
            "backup_type": j.backup_type,
            "status": j.status,
            "size_mb": j.size_mb,
            "created_at": j.created_at.strftime("%Y-%m-%d %H:%M:%S") if j.created_at else "",
            "completed_at": j.completed_at.strftime("%Y-%m-%d %H:%M:%S") if j.completed_at else ""
        })
    return results

class ScheduleCreate(BaseModel):
    project_id: int
    schedule_expression: str
    backup_type: str
    retention_days: int

@app.post("/api/backups/schedules", dependencies=[Depends(verify_credentials)])
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)):
    from models import BackupSchedule
    proj = db.query(Project).filter(Project.id == payload.project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    sched = BackupSchedule(
        project_id=proj.id,
        cluster_name=proj.name,
        schedule_expression=payload.schedule_expression,
        backup_type=payload.backup_type,
        retention_days=payload.retention_days
    )
    db.add(sched)
    db.commit()
    return {"success": True, "message": "Schedule created"}

@app.get("/api/backups/schedules", dependencies=[Depends(verify_credentials)])
def get_schedules(db: Session = Depends(get_db)):
    from models import BackupSchedule
    scheds = db.query(BackupSchedule).order_by(BackupSchedule.id.desc()).all()
    results = []
    for s in scheds:
        results.append({
            "id": s.id,
            "project_id": s.project_id,
            "cluster_name": s.cluster_name,
            "schedule_expression": s.schedule_expression,
            "backup_type": s.backup_type,
            "retention_days": s.retention_days,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else ""
        })
    return results
"""

if "@app.post(\"/api/backups\"" not in content:
    content += "\n" + backup_apis
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Backup APIs to main.py")
else:
    print("Backup APIs already exist")
