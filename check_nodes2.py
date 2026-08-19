import os, sys
os.environ['VAULT_KEY'] = 'aT5XEmyjit99aWs2ej5QBCP84X--0HmFMXGDZNNX8j0='
os.environ['DATABASE_URL'] = 'sqlite:///./fastapi_app.db'

sys.path.insert(0, '.')
os.chdir('fastapi_app')
from models import SessionLocal, DatabaseNode, Project
from vault import encrypt, decrypt

db = SessionLocal()
projects = db.query(Project).all()
for p in projects:
    print(f"Project {p.id}: {p.name}")
    for n in p.nodes:
        decrypted = decrypt(n.encrypted_url) if n.encrypted_url else "EMPTY"
        print(f"  Node {n.id}: {n.name} ({n.role}) - URL: {str(decrypted)[:70]}...")
db.close()
