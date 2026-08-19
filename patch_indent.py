import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the tasks.append indentation
content = content.replace("          tasks.append(get_server_metrics(node_dict, project_id=proj.id))", "        tasks.append(get_server_metrics(node_dict, project_id=proj.id))")

# Wait, let's also check get_single_node_metrics
old_single = """    node_dict = {
        'id': node.id,
        'name': node.name,
        'role': node.role,
        'encrypted_url': node.encrypted_url,
        'ssh_host': node.ssh_host,
        'ssh_port': node.ssh_port,
        'ssh_username': node.ssh_username,
        'encrypted_ssh_credential': node.encrypted_ssh_credential,
        'metric_table': node.project.metric_table if node.project else None
    }
    metrics = await get_server_metrics(node_dict, project_id=node.project_id)"""

# In get_single_node_metrics, it's inside `def get_single_node_metrics` so 4 spaces. The patch was exactly 4 spaces. It should be fine.
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed indentation")
