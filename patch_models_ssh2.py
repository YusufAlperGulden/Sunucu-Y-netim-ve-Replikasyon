import re

models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_fields = """    # ?ifrelenmiY veritaban baYlant metni
    encrypted_url = Column(String(500))"""

new_fields = """    # Şifrelenmiş veritabanı bağlantı metni
    encrypted_url = Column(String(500))
    
    # SSH Credentials for OS-level access
    ssh_host = Column(String(255), nullable=True)
    ssh_port = Column(Integer, default=22)
    ssh_username = Column(String(255), default="root")
    encrypted_ssh_credential = Column(String, nullable=True)"""

if "ssh_host = Column" not in content:
    content = re.sub(r'    #.*?encrypted_url = Column\(String\(500\)\)', new_fields, content, flags=re.DOTALL)
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added SSH fields to models.py")
else:
    print("Already exists")
