import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

endpoints = """
@app.get("/api/projects/{project_id}/settings")
def get_project_settings(project_id: int, db: Session = Depends(get_db)):
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if not ps:
        # Default settings if none exist
        default_settings = {
            "backup_cloud_retention": "180",
            "backup_retention": "31",
            "backupdir": "/home/cmon/backups",
            "pgbackrest_cipher_pass": "********",
            "pgbackrest_cipher_type": "none",
            "pgbackrest_repo_hostname": "",
            "pgbackrest_repo_path": "",
            "pgbackrest_stanza_name": "",
            "pitr_retention_hours": ""
        }
        return default_settings
    try:
        data = json.loads(ps.settings_json)
        return data
    except:
        return {}

@app.put("/api/projects/{project_id}/settings")
async def update_project_settings(project_id: int, request: Request, db: Session = Depends(get_db)):
    from models import ProjectSettings
    import json
    data = await request.json()
    
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if not ps:
        ps = ProjectSettings(project_id=project_id, settings_json=json.dumps(data))
        db.add(ps)
    else:
        # Merge settings
        try:
            current_data = json.loads(ps.settings_json)
        except:
            current_data = {}
        current_data.update(data)
        ps.settings_json = json.dumps(current_data)
        
    db.commit()
    return {"status": "ok"}
"""

if "def get_project_settings" not in content:
    content += "\n" + endpoints
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added settings API endpoints")
else:
    print("Endpoints already exist")
