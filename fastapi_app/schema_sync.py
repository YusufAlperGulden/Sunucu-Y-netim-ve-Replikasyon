import asyncio
from sqlalchemy import create_engine, MetaData
from vault import decrypt
from models import SessionLocal, Project

def sync_schema(primary_url, standby_url):
    print("Connecting to primary to reflect schema...")
    # Change postgres:// to postgresql:// for sqlalchemy
    primary_url_sa = primary_url.replace("postgres://", "postgresql://")
    standby_url_sa = standby_url.replace("postgres://", "postgresql://")
    
    engine_primary = create_engine(primary_url_sa)
    engine_standby = create_engine(standby_url_sa)
    
    metadata = MetaData()
    metadata.reflect(bind=engine_primary)
    
    print(f"Found {len(metadata.tables)} tables. Creating on standby...")
    metadata.create_all(bind=engine_standby)
    print("Schema sync complete!")

if __name__ == "__main__":
    db = SessionLocal()
    proj = db.query(Project).first()
    primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
    standby = next((n for n in proj.nodes if n.role.lower() == 'standby'), None)
    
    if primary and standby:
        p_url = decrypt(primary.encrypted_url)
        s_url = decrypt(standby.encrypted_url)
        sync_schema(p_url, s_url)
    db.close()
