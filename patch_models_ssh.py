import re

model_path = 'fastapi_app/models.py'
with open(model_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will add SSH fields to DatabaseNode
new_fields = """
    # SSH Infrastructure Fields
    ssh_host = Column(String(255), nullable=True)
    ssh_port = Column(Integer, default=22)
    ssh_username = Column(String(255), default='root')
    encrypted_ssh_credential = Column(String, nullable=True) # AES encrypted password or PEM key
"""

if "ssh_host = Column" not in content:
    content = content.replace("encrypted_url = Column(String)", "encrypted_url = Column(String)\n" + new_fields)
    with open(model_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added SSH fields to DatabaseNode")
else:
    print("Already added")
