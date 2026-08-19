import re

# Add a debug endpoint that shows the raw metric error
main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

debug_endpoint = """
@app.get("/api/debug/metrics/{project_id}", dependencies=[Depends(verify_credentials)])
async def debug_metrics(project_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    from vault import decrypt
    import asyncio
    
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return {"error": "Project not found"}
    
    results = []
    for node in proj.nodes:
        url = decrypt(node.encrypted_url) if node.encrypted_url else None
        node_dict = {
            'id': node.id, 'name': node.name, 'role': node.role,
            'encrypted_url': node.encrypted_url,
            'ssh_host': node.ssh_host, 'ssh_port': node.ssh_port,
            'ssh_username': node.ssh_username,
            'encrypted_ssh_credential': node.encrypted_ssh_credential,
            'metric_table': proj.metric_table
        }
        metrics = await get_server_metrics(node_dict, project_id=proj.id)
        results.append({
            "node_id": node.id,
            "node_name": node.name,
            "has_url": bool(node.encrypted_url),
            "decrypted_url_preview": url[:30] + "..." if url and len(url) > 30 else url,
            "metrics": metrics
        })
    return results
"""

if "@app.get(\"/api/debug/metrics" not in content:
    content += "\n" + debug_endpoint
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added debug metrics endpoint")
else:
    print("Already exists")
