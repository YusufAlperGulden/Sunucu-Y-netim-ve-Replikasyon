import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to change the add_node signature to inject BackgroundTasks
old_add_node_sig = """@app.post("/api/projects/{project_id}/nodes", dependencies=[Depends(verify_credentials)])
async def add_node(project_id: int, node: NodeCreate, db: Session = Depends(get_db)):"""

new_add_node_sig = """@app.post("/api/projects/{project_id}/nodes", dependencies=[Depends(verify_credentials)])
async def add_node(project_id: int, node: NodeCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):"""

content = content.replace(old_add_node_sig, new_add_node_sig)

# We need to inject the logic to call apply_postgres_settings
old_add_node_return = """    db.commit()
    return {"success": True}"""

new_add_node_return = """    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": new_node.id, "encrypted_url": new_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True}"""

content = content.replace(old_add_node_return, new_add_node_return)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated add_node to apply settings")
