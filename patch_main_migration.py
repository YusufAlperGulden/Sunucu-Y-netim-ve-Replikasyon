import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = """@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup complete.")
    from sqlalchemy import text
    from database import engine
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE nodes ADD COLUMN ssh_host VARCHAR(255)"))
            conn.execute(text("ALTER TABLE nodes ADD COLUMN ssh_port INTEGER DEFAULT 22"))
            conn.execute(text("ALTER TABLE nodes ADD COLUMN ssh_username VARCHAR(255) DEFAULT 'root'"))
            conn.execute(text("ALTER TABLE nodes ADD COLUMN encrypted_ssh_credential VARCHAR"))
        except Exception as e:
            pass # column already exists
            
        try:
            conn.execute(text("ALTER TABLE audit_logs ADD COLUMN username VARCHAR(50) DEFAULT 'system'"))
        except Exception as e:
            pass # column already exists
    yield
    # Shutdown
"""

if "ALTER TABLE nodes ADD COLUMN ssh_host" not in content:
    content = re.sub(r'@asynccontextmanager\nasync def lifespan.*?# Shutdown', migration_code, content, flags=re.DOTALL)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added migrations to lifespan")
else:
    print("Migrations already exist")
