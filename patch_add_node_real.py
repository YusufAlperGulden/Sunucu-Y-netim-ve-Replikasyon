import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_add_node_return = """    db.commit()
    
    return {"success": True, "message": "Node added securely."}"""

new_add_node_return = """    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": db_node.id, "encrypted_url": db_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True, "message": "Node added securely."}"""

if "db.commit()\n    \n    return {\"success\": True" in content:
    content = content.replace(old_add_node_return, new_add_node_return)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed add_node successfully")
else:
    # Try different whitespace
    content = re.sub(r'db\.commit\(\)\s*return \{"success": True, "message": "Node added securely\."\}', new_add_node_return, content)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed add_node successfully with regex")
