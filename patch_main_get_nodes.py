import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Edit get_project_detail nodes.append
old_nodes_append = """        nodes.append({
            "id": n.id, 
            "role": n.role, 
            "name": n.name,
            "ip": ip,
            "port": port,
            "type": db_type,
            "status": "Operational",
            "version": "16.4" # Or fetch from DB if available
        })"""
new_nodes_append = """        nodes.append({
            "id": n.id, 
            "role": n.role, 
            "name": n.name,
            "ip": ip,
            "port": port,
            "type": db_type,
            "status": "Operational",
            "version": "16.4", # Or fetch from DB if available
            "ssh_host": n.ssh_host,
            "ssh_port": n.ssh_port,
            "ssh_username": n.ssh_username,
            "has_ssh_credential": bool(n.encrypted_ssh_credential)
        })"""
content = content.replace(old_nodes_append, new_nodes_append)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated get_project_detail")
