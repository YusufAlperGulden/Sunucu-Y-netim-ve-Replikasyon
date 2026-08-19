import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

apply_settings_func = """
async def apply_postgres_settings(nodes, settings_data):
    import asyncpg
    from vault import decrypt
    
    # Define which settings map to actual PostgreSQL parameters
    pg_params = [
        'log_min_duration_statement',
        'wal_level',
        'max_replication_slots',
        'max_wal_senders',
        'shared_buffers',
        'work_mem',
        'max_connections'
    ]
    
    for node in nodes:
        db_url = decrypt(node.encrypted_url)
        try:
            conn = await asyncpg.connect(db_url, timeout=5.0)
            
            for param in pg_params:
                if param in settings_data and settings_data[param]:
                    # Prevent SQL injection loosely by removing quotes
                    safe_val = str(settings_data[param]).replace("'", "").strip()
                    try:
                        await conn.execute(f"ALTER SYSTEM SET {param} = '{safe_val}';")
                    except Exception as e:
                        print(f"Error setting {param} on node {node.id}: {e}")
                        
            # Reload configuration (Note: some settings like shared_buffers require a full restart to take effect,
            # but pg_reload_conf() is safe to call and applies dynamic ones immediately).
            await conn.execute("SELECT pg_reload_conf();")
            await conn.close()
            print(f"Successfully applied settings to node {node.id}")
        except Exception as e:
            print(f"Failed to connect and apply settings to node {node.id}: {e}")

"""

# Now replace the update endpoint to call this function
old_put_endpoint = """@app.put("/api/projects/{project_id}/settings")
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
    return {"status": "ok"}"""

new_put_endpoint = """@app.put("/api/projects/{project_id}/settings")
async def update_project_settings(project_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from models import ProjectSettings, DatabaseNode
    import json
    data = await request.json()
    
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if not ps:
        current_data = {}
        current_data.update(data)
        ps = ProjectSettings(project_id=project_id, settings_json=json.dumps(current_data))
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
    
    # Fetch all nodes and apply PostgreSQL parameters asynchronously
    nodes = db.query(DatabaseNode).filter(DatabaseNode.project_id == project_id).all()
    if nodes:
        background_tasks.add_task(apply_postgres_settings, nodes, current_data)
        
    return {"status": "ok"}"""

if apply_settings_func not in content:
    # Insert function before the endpoints
    content = content.replace(old_put_endpoint, apply_settings_func + "\n" + new_put_endpoint)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added apply_postgres_settings and updated PUT endpoint")
else:
    print("Already added")
