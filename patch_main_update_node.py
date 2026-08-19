import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update NodeUpdate schema
old_schema = """class NodeUpdate(BaseModel):
    url: str
    name: Optional[str] = None
    is_primary: Optional[bool] = None"""
new_schema = """class NodeUpdate(BaseModel):
    url: str
    name: Optional[str] = None
    is_primary: Optional[bool] = None
    ssh_host: Optional[str] = None
    ssh_port: Optional[int] = 22
    ssh_username: Optional[str] = 'root'
    ssh_credential: Optional[str] = None"""
content = content.replace(old_schema, new_schema)

# Inside update_node_url
old_update = """    node.encrypted_url = encrypt(update.url)
    if update.name is not None:
        node.name = update.name
    if update.is_primary is not None:
        node.is_primary = update.is_primary
    
    db.commit()"""
new_update = """    node.encrypted_url = encrypt(update.url)
    if update.name is not None:
        node.name = update.name
    if update.is_primary is not None:
        node.is_primary = update.is_primary
        
    if update.ssh_host is not None:
        node.ssh_host = update.ssh_host
    if update.ssh_port is not None:
        node.ssh_port = update.ssh_port
    if update.ssh_username is not None:
        node.ssh_username = update.ssh_username
    if update.ssh_credential:
        node.encrypted_ssh_credential = encrypt(update.ssh_credential)
    elif update.ssh_credential == "":
        node.encrypted_ssh_credential = None
        
    db.commit()"""
content = content.replace(old_update, new_update)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated NodeUpdate and endpoint")

