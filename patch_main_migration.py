import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = """
    # Run automatic ALTER TABLE migrations to fix missing columns
    db = SessionLocal()
    try:
        db.execute(text("ALTER TABLE database_nodes ADD COLUMN ssh_host VARCHAR(255);"))
        db.commit()
    except Exception:
        db.rollback()
        
    try:
        db.execute(text("ALTER TABLE database_nodes ADD COLUMN ssh_port INTEGER DEFAULT 22;"))
        db.commit()
    except Exception:
        db.rollback()
        
    try:
        db.execute(text("ALTER TABLE database_nodes ADD COLUMN ssh_username VARCHAR(255) DEFAULT 'root';"))
        db.commit()
    except Exception:
        db.rollback()
        
    try:
        db.execute(text("ALTER TABLE database_nodes ADD COLUMN encrypted_ssh_credential VARCHAR;"))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
"""

# Find lifespan
old_lifespan = """async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield"""
new_lifespan = """async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    from sqlalchemy.sql import text
    from database import SessionLocal
""" + migration_code + """
    yield"""

if "ALTER TABLE database_nodes" not in content:
    content = content.replace(old_lifespan, new_lifespan)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added DB migration code to lifespan")
else:
    print("Already added")
