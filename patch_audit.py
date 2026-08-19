import re
models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "username = Column(String(50), nullable=True)" not in content:
    content = content.replace('details = Column(String(500))', 'details = Column(String(500))\n    username = Column(String(50), nullable=True, default="system")')
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added username to AuditLog")
else:
    print("username already in AuditLog")
