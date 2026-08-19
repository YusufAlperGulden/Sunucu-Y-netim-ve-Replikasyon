import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_call = "tasks.append(get_server_metrics(node.encrypted_url, project_id=proj.id, role=node.role, metric_table=proj.metric_table))"

new_call = """node_dict = {
              'id': node.id,
              'name': node.name,
              'role': node.role,
              'encrypted_url': node.encrypted_url,
              'ssh_host': node.ssh_host,
              'ssh_port': node.ssh_port,
              'ssh_username': node.ssh_username,
              'encrypted_ssh_credential': node.encrypted_ssh_credential,
              'metric_table': proj.metric_table
          }
          tasks.append(get_server_metrics(node_dict, project_id=proj.id))"""

if old_call in content:
    content = content.replace(old_call, new_call)
    
    # Also fix the map results back to node definitions:
    # 'id': node['id'] is wrong, it's node.id because it's a sqlalchemy object
    old_id = "'id': node['id'],"
    new_id = "'id': node.id,"
    content = content.replace(old_id, new_id)
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated main.py")
else:
    print("Could not find old_call")
