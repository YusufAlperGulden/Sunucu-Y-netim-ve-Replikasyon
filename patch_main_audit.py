import re
main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_get_audit = """def get_audit_logs(db: Session = Depends(get_db)):
    from models import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.isoformat() if l.timestamp else None, 'action': l.action, 'details': l.details} for l in logs]"""

new_get_audit = """def get_audit_logs(db: Session = Depends(get_db)):
    from models import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.strftime("%Y-%m-%d %H:%M:%S") if l.timestamp else "-", 'action': l.action, 'details': l.details, 'user': l.username or "System"} for l in logs]"""

if "def get_audit_logs" in content:
    content = content.replace(old_get_audit, new_get_audit)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated get_audit_logs")
else:
    print("get_audit_logs not found")
