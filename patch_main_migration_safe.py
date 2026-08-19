import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

safe_migration = """@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup complete.")
    from sqlalchemy import text
    from models import engine
    with engine.begin() as conn:
        for stmt in [
            "ALTER TABLE nodes ADD COLUMN ssh_host VARCHAR(255)",
            "ALTER TABLE nodes ADD COLUMN ssh_port INTEGER DEFAULT 22",
            "ALTER TABLE nodes ADD COLUMN ssh_username VARCHAR(255) DEFAULT 'root'",
            "ALTER TABLE nodes ADD COLUMN encrypted_ssh_credential VARCHAR",
            "ALTER TABLE audit_logs ADD COLUMN username VARCHAR(50) DEFAULT 'system'"
        ]:
            try:
                conn.execute(text(stmt))
            except Exception:
                pass
    yield
    # Shutdown"""

content = re.sub(r'@asynccontextmanager\nasync def lifespan.*?# Shutdown', safe_migration, content, flags=re.DOTALL)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Made migrations safe per-column")
