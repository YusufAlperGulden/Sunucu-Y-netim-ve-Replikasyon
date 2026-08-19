import os, sys
os.environ['VAULT_KEY'] = 'aT5XEmyjit99aWs2ej5QBCP84X--0HmFMXGDZNNX8j0='
os.environ['DATABASE_URL'] = 'sqlite:///./fastapi_app.db'
os.environ['ADMIN_USER'] = 'admin'
os.environ['ADMIN_PASS'] = 'admin'

sys.path.insert(0, 'fastapi_app')
from fastapi_app.models import SessionLocal, DatabaseNode, Project
from fastapi_app.vault import encrypt, decrypt

db = SessionLocal()

# Show all projects and nodes
projects = db.query(Project).all()
for p in projects:
    print(f"Project {p.id}: {p.name}")
    for n in p.nodes:
        decrypted = decrypt(n.encrypted_url) if n.encrypted_url else None
        print(f"  Node {n.id}: {n.name} ({n.role}) - URL: {decrypted[:60] if decrypted else 'EMPTY'}...")
        
db.close()
