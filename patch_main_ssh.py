import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# NodeCreate schema
old_schema = """class NodeCreate(BaseModel):
    project_id: int
    name: str
    url: str
    is_primary: bool = False
"""
new_schema = """class NodeCreate(BaseModel):
    project_id: int
    name: str
    url: str
    is_primary: bool = False
    ssh_host: Optional[str] = None
    ssh_port: int = 22
    ssh_username: str = 'root'
    ssh_credential: Optional[str] = None
"""
content = content.replace(old_schema, new_schema)

# Inside add_node
old_add = """    enc_url = encrypt(node.url)
    
    new_node = DatabaseNode(
        project_id=node.project_id,
        name=node.name,
        encrypted_url=enc_url,
        is_primary=node.is_primary,
        status="Unknown"
    )"""
new_add = """    enc_url = encrypt(node.url)
    enc_ssh = encrypt(node.ssh_credential) if node.ssh_credential else None
    
    new_node = DatabaseNode(
        project_id=node.project_id,
        name=node.name,
        encrypted_url=enc_url,
        is_primary=node.is_primary,
        status="Unknown",
        ssh_host=node.ssh_host,
        ssh_port=node.ssh_port,
        ssh_username=node.ssh_username,
        encrypted_ssh_credential=enc_ssh
    )"""
content = content.replace(old_add, new_add)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.py schema and add_node")

