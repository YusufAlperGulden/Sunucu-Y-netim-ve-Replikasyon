import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_single_call = """    metrics = await get_server_metrics(
        node.encrypted_url,
        project_id=node.project_id,
        role=node.role,
        metric_table=node.project.metric_table if node.project else None
    )"""

new_single_call = """    node_dict = {
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

if old_single_call in content:
    content = content.replace(old_single_call, new_single_call)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated single node call")
else:
    print("Could not find single call")
