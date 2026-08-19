import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_get_node = """    return {
        "id": node.id, 
        "url": decrypt(node.encrypted_url),
        "name": node.name,
        "is_primary": node.is_primary
    }"""
new_get_node = """    return {
        "id": node.id, 
        "url": decrypt(node.encrypted_url),
        "name": node.name,
        "is_primary": node.is_primary,
        "ssh_host": node.ssh_host or "",
        "ssh_port": node.ssh_port or 22,
        "ssh_username": node.ssh_username or "root",
        "has_ssh_credential": bool(node.encrypted_ssh_credential)
    }"""
content = content.replace(old_get_node, new_get_node)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated get_node_url")

