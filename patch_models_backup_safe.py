models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

backup_models = """
class BackupJob(Base):
    __tablename__ = 'backup_jobs'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cluster_name = Column(String(255))
    backup_type = Column(String(50)) # FULL, INCR, DIFF
    status = Column(String(50), default="IN_PROGRESS") # COMPLETED, FAILED, IN_PROGRESS
    size_mb = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
class BackupSchedule(Base):
    __tablename__ = 'backup_schedules'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cluster_name = Column(String(255))
    schedule_expression = Column(String(100)) # e.g. "Daily at 02:00 AM"
    backup_type = Column(String(50))
    retention_days = Column(Integer, default=7)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

if "class BackupJob" not in content:
    content += "\n" + backup_models
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Backup models")
