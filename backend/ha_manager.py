import time
from sqlalchemy import create_engine, text
from urllib.parse import urlsplit

def normalize(url: str) -> str:
    if not url:
        return None
    url = url.strip()
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url

def check_db_health(url: str):
    if not url:
        return False, 0
    n_url = normalize(url)
    try:
        start_time = time.time()
        engine = create_engine(n_url, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        latency = int((time.time() - start_time) * 1000)
        engine.dispose()
        return True, latency
    except Exception:
        return False, 0

def initialize_replication(primary_url: str, standby_url: str, pub_name="universal_pub", sub_name="universal_sub"):
    """
    Sets up logical replication from Primary to Standby for all tables.
    """
    try:
        engine_master = create_engine(normalize(primary_url), isolation_level="AUTOCOMMIT", pool_pre_ping=True)
        with engine_master.connect() as conn:
            try:
                conn.execute(text(f"DROP PUBLICATION IF EXISTS {pub_name};"))
            except: pass
            conn.execute(text(f"CREATE PUBLICATION {pub_name} FOR ALL TABLES;"))
            
        time.sleep(2)
        
        clean_master = primary_url.replace('?sslmode=require&channel_binding=require', '').replace('?sslmode=require', '')
        
        engine_standby = create_engine(normalize(standby_url), isolation_level="AUTOCOMMIT", pool_pre_ping=True)
        with engine_standby.connect() as conn:
            try:
                conn.execute(text(f"ALTER SUBSCRIPTION {sub_name} DISABLE"))
            except: pass
            try:
                conn.execute(text(f"DROP SUBSCRIPTION IF EXISTS {sub_name};"))
            except: pass
            
            conn.execute(text(f"CREATE SUBSCRIPTION {sub_name} CONNECTION '{clean_master}' PUBLICATION {pub_name} WITH (copy_data = true);"))
            
        return True, "Replication successfully initialized."
    except Exception as e:
        return False, str(e)
