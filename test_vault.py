import os, sys
sys.path.insert(0, 'fastapi_app')
os.environ['VAULT_KEY'] = 'aT5XEmyjit99aWs2ej5QBCP84X--0HmFMXGDZNNX8j0='
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['ADMIN_USER'] = 'admin'
os.environ['ADMIN_PASS'] = 'admin'

from fastapi_app.vault import encrypt, decrypt

FRANKFURT = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

enc_f = encrypt(FRANKFURT)
enc_y = encrypt(YEDEK)

dec_f = decrypt(enc_f)
dec_y = decrypt(enc_y)

print("FRANKFURT encrypt OK:", dec_f == FRANKFURT)
print("YEDEK encrypt OK:", dec_y == YEDEK)
print()
print("Encrypted FRANKFURT:", enc_f[:40] + "...")
print("Encrypted YEDEK:", enc_y[:40] + "...")
