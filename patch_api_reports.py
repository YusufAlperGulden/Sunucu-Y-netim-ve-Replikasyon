import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

api_code = """
class ReportCreate(BaseModel):
    project_id: int
    report_type: str
    data_range_days: int
    recipients: str

@app.post("/api/reports", dependencies=[Depends(verify_credentials)])
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    from models import OperationalReport
    import datetime
    
    # Generate a dummy filename based on type and time
    safe_type = report.report_type.replace(" ", "_").lower()
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{safe_type}_{ts}.pdf"
    
    new_report = OperationalReport(
        project_id=report.project_id,
        report_type=report.report_type,
        data_range_days=report.data_range_days,
        recipients=report.recipients,
        file_name=filename,
        created_by="admin"
    )
    db.add(new_report)
    db.commit()
    return {"success": True, "message": "Report created"}

@app.get("/api/reports", dependencies=[Depends(verify_credentials)])
def get_reports(db: Session = Depends(get_db)):
    from models import OperationalReport, Project
    reports = db.query(OperationalReport).order_by(OperationalReport.created_at.desc()).all()
    
    result = []
    for r in reports:
        # Get cluster name
        proj = db.query(Project).filter(Project.id == r.project_id).first()
        cluster_name = proj.name if proj else "Unknown Cluster"
        
        result.append({
            "id": r.id,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
            "file_name": r.file_name,
            "report_type": r.report_type,
            "cluster": cluster_name,
            "created_by": r.created_by,
            "data_range": f"Last {r.data_range_days} days",
            "recipients": r.recipients or "-"
        })
    return result
"""

if "@app.post(\"/api/reports\"" not in content:
    content += "\n" + api_code
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added report endpoints")
else:
    print("Already added")
