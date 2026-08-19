import os, asyncio, sys
os.environ['VAULT_KEY'] = 'aT5XEmyjit99aWs2ej5QBCP84X--0HmFMXGDZNNX8j0='
os.environ['DATABASE_URL'] = 'sqlite:///./fastapi_app.db'
os.environ['ADMIN_USER'] = 'admin'
os.environ['ADMIN_PASS'] = 'admin'

sys.path.insert(0, 'fastapi_app')
from fastapi_app.vault import encrypt
from sqlalchemy import create_engine, text

FRANKFURT = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

enc_f = encrypt(FRANKFURT)
enc_y = encrypt(YEDEK)

print("Encrypted FRANKFURT:", enc_f)
print()
print("Encrypted YEDEK:", enc_y)
