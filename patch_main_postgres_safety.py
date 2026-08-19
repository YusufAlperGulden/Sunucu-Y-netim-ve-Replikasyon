import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_put_endpoint = """    # Fetch all nodes and apply PostgreSQL parameters asynchronously
    nodes = db.query(DatabaseNode).filter(DatabaseNode.project_id == project_id).all()
    if nodes:
        background_tasks.add_task(apply_postgres_settings, nodes, current_data)
        
    return {"status": "ok"}"""

new_put_endpoint = """    # Fetch all nodes and apply PostgreSQL parameters asynchronously
    nodes = db.query(DatabaseNode).filter(DatabaseNode.project_id == project_id).all()
    if nodes:
        # Pass a list of dicts to avoid DetachedInstanceError in background task
        safe_nodes = [{"id": n.id, "encrypted_url": n.encrypted_url} for n in nodes]
        background_tasks.add_task(apply_postgres_settings, safe_nodes, current_data)
        
    return {"status": "ok"}"""

content = content.replace(old_put_endpoint, new_put_endpoint)

# Also update the function to accept dicts
old_func = """    for node in nodes:
        db_url = decrypt(node.encrypted_url)
        try:
            conn = await asyncpg.connect(db_url, timeout=5.0)"""

new_func = """    for node in nodes:
        db_url = decrypt(node['encrypted_url'])
        try:
            conn = await asyncpg.connect(db_url, timeout=5.0)"""

content = content.replace(old_func, new_func)

# And replace `node.id` with `node['id']`
content = content.replace("node.id", "node['id']")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Made ORM nodes safe for background task")
