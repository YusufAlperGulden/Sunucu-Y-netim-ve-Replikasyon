import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The two Neon URLs
FRANKFURT = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

neon_sync_code = f"""
    # Auto-sync Neon URLs if nodes exist but have wrong/old URLs
    try:
        from vault import encrypt, decrypt
        from models import SessionLocal, DatabaseNode, Project
        db = SessionLocal()
        try:
            projects = db.query(Project).all()
            for proj in projects:
                nodes = proj.nodes
                if len(nodes) >= 2:
                    primary_nodes = [n for n in nodes if n.role and n.role.lower() == 'primary']
                    standby_nodes = [n for n in nodes if n.role and n.role.lower() == 'standby']
                    
                    FRANKFURT_URL = "{FRANKFURT}"
                    YEDEK_URL = "{YEDEK}"
                    
                    for node in primary_nodes:
                        current = decrypt(node.encrypted_url) if node.encrypted_url else None
                        if current != FRANKFURT_URL:
                            node.encrypted_url = encrypt(FRANKFURT_URL)
                            print(f"Updated primary node {{node.id}} URL to Frankfurt (Neon)")
                    
                    for node in standby_nodes:
                        current = decrypt(node.encrypted_url) if node.encrypted_url else None
                        if current != YEDEK_URL:
                            node.encrypted_url = encrypt(YEDEK_URL)
                            print(f"Updated standby node {{node.id}} URL to Yedek (Neon)")
                    
                    db.commit()
                    
                    # Also set metric_table if not set
                    if not proj.metric_table:
                        proj.metric_table = 'vehicles'
                        db.commit()
                        print(f"Set metric_table=vehicles for project {{proj.id}}")
        finally:
            db.close()
    except Exception as e:
        print(f"Neon URL sync error: {{e}}")
"""

old_yield = """    try:
                conn.execute(text(stmt))
            except Exception:
                pass
    yield
    # Shutdown"""

new_yield = """    try:
                conn.execute(text(stmt))
            except Exception:
                pass
    """ + neon_sync_code.strip() + """
    yield
    # Shutdown"""

if "Auto-sync Neon URLs" not in content:
    content = content.replace(old_yield, new_yield)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Neon URL auto-sync to lifespan")
else:
    print("Already exists")
