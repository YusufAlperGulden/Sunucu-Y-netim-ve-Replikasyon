import asyncpg
import asyncio
from vault import decrypt
from urllib.parse import urlparse
from sqlalchemy import create_engine, MetaData

async def test_connection(db_url: str) -> bool:
    """Verilen PostgreSQL URL'sine ping atarak bağlantıyı test eder."""
    try:
        # asyncpg.connect requires timeout to prevent hanging
        conn = await asyncpg.connect(db_url, timeout=5.0)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

async def setup_replication(primary_encrypted_url: str, standby_encrypted_url: str) -> dict:
    """İki sunucu arasında PUBLICATION ve SUBSCRIPTION tünellerini (Logical Replication) kurar."""
    try:
        primary_url = decrypt(primary_encrypted_url)
        standby_url = decrypt(standby_encrypted_url)
        
        if not primary_url or not standby_url:
            return {"success": False, "message": "Failed to decrypt URLs"}

        # 0. Şema Senkronizasyonu (Schema Sync)
        try:
            await asyncio.to_thread(sync_schema_between_dbs, primary_url, standby_url)
        except Exception as schema_err:
            print(f"Schema sync error: {schema_err}")
            return {"success": False, "message": f"Schema sync failed: {str(schema_err)}"}

        # 1. Primary Sunucuya Bağlan ve PUBLICATION oluştur (ALL TABLES)
        # asyncpg ile bağlan
        p_conn = await asyncpg.connect(primary_url, timeout=10.0)
        try:
            # Drop existing if any, then create (for idempotency)
            await p_conn.execute("DROP PUBLICATION IF EXISTS universal_pub;")
            await p_conn.execute("CREATE PUBLICATION universal_pub FOR ALL TABLES;")
        finally:
            await p_conn.close()

        # 2. Standby Sunucuya Bağlan ve SUBSCRIPTION oluştur
        # Standby'a bağlanırken bağlantı bilgisinden sslmode vs ayrıştırmak gerekebilir ama
        # PostgreSQL CONNECTION stringi as-is formatında kabul eder. Sadece güvenlik için
        # sslmode=prefer vb parse edilebilir. Şimdilik doğrudan veriyoruz.
        s_conn = await asyncpg.connect(standby_url, timeout=10.0)
        try:
            await s_conn.execute("DROP SUBSCRIPTION IF EXISTS universal_sub;")
            
            # create subscription query
            # PostgreSQL requires the connection string in single quotes
            safe_primary_url = primary_url.replace("'", "''")
            sub_query = f"CREATE SUBSCRIPTION universal_sub CONNECTION '{safe_primary_url}' PUBLICATION universal_pub;"
            await s_conn.execute(sub_query)
        finally:
            await s_conn.close()

        return {"success": True, "message": "Logical replication (ALL TABLES) established successfully."}

    except Exception as e:
        print(f"Replication setup error: {e}")
        return {"success": False, "message": f"Setup failed: {str(e)}"}

def sync_schema_between_dbs(primary_url: str, standby_url: str):
    """SQLAlchemy MetaData Reflection kullanarak şemaları kopyalar (Sadece iskelet)."""
    # asyncpg url (postgres://) ile sqlalchemy url (postgresql://) uyumu
    p_url = primary_url.replace("postgres://", "postgresql://")
    s_url = standby_url.replace("postgres://", "postgresql://")

    engine_primary = create_engine(p_url)
    engine_standby = create_engine(s_url)

    metadata = MetaData()
    # Primary'den tablo yapılarını oku
    metadata.reflect(bind=engine_primary)
    
    # Standby'da aynı tabloları yarat (Var olanları atlar - checkfirst=True varsayılandır)
    metadata.create_all(bind=engine_standby)
    print(f"Schema sync completed. Processed {len(metadata.tables)} tables.")

async def check_and_protect_wal_bloat(primary_encrypted_url: str, max_wal_lag_mb: int) -> dict:
    """Primary sunucuya bağlanarak WAL lag'i ölçer. Kritik seviyeyi aşarsa slot'u koparır."""
    try:
        primary_url = decrypt(primary_encrypted_url)
        if not primary_url:
            return {"success": False, "message": "Failed to decrypt URL", "dropped": False}

        conn = await asyncpg.connect(primary_url, timeout=5.0)
        try:
            # Replikasyon gecikmesini byte cinsinden hesaplayan PostgreSQL sorgusu
            # universal_sub adlı subscription için universal_sub slotu oluşuyor
            query = """
                SELECT slot_name, 
                       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes 
                FROM pg_replication_slots 
                WHERE slot_name = 'universal_sub';
            """
            row = await conn.fetchrow(query)
            
            if not row or row['lag_bytes'] is None:
                return {"success": True, "message": "Replication slot not found or inactive.", "dropped": False, "lag_mb": 0}
            
            lag_mb = row['lag_bytes'] / (1024 * 1024)
            
            # Kritik eşiği aştı mı?
            if lag_mb > max_wal_lag_mb:
                # ACİL DURUM: DROP SLOT
                print(f"[CRITICAL] WAL lag ({lag_mb:.2f} MB) exceeded max limit ({max_wal_lag_mb} MB). Dropping slot!")
                await conn.execute("SELECT pg_drop_replication_slot('universal_sub');")
                return {"success": True, "message": f"CRITICAL: Slot dropped to prevent WAL bloat. Lag was {lag_mb:.2f} MB", "dropped": True, "lag_mb": lag_mb}
            else:
                return {"success": True, "message": f"Lag is healthy ({lag_mb:.2f} MB)", "dropped": False, "lag_mb": lag_mb}
                
        finally:
            await conn.close()

    except Exception as e:
        print(f"WAL Bloat check error: {e}")
        return {"success": False, "message": f"Check failed: {str(e)}", "dropped": False}

import time

async def get_server_metrics(encrypted_url: str) -> dict:
    try:
        url = decrypt(encrypted_url)
        if not url:
            return {'status': 'offline', 'error': 'Decryption failed'}
        
        start_time = time.time()
        conn = await asyncpg.connect(url, timeout=5.0)
        end_time = time.time()
        ping_ms = int((end_time - start_time) * 1000)
        
        try:
            db_size_row = await conn.fetchrow('SELECT pg_database_size(current_database()) as size')
            db_size_kb = db_size_row['size'] / 1024 if db_size_row and db_size_row['size'] else 0
            
            conn_row = await conn.fetchrow("SELECT count(*) as active, (SELECT setting::int FROM pg_settings WHERE name='max_connections') as max FROM pg_stat_activity")
            active_conn = conn_row['active'] if conn_row else 0
            max_conn = conn_row['max'] if conn_row else 100
            
            stat_row = await conn.fetchrow('SELECT blks_hit, blks_read, xact_commit, xact_rollback FROM pg_stat_database WHERE datname = current_database()')
            if stat_row:
                total_blks = stat_row['blks_hit'] + stat_row['blks_read']
                cache_hit = (stat_row['blks_hit'] / total_blks * 100) if total_blks > 0 else 100.0
                commits = stat_row['xact_commit']
                rollbacks = stat_row['xact_rollback']
            else:
                cache_hit, commits, rollbacks = 100.0, 0, 0
                
            ver_row = await conn.fetchrow('SELECT version()')
            version_str = ver_row['version'].split('on')[0].strip() if ver_row else 'Unknown'
            
            uptime_row = await conn.fetchrow("SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime")
            uptime = str(uptime_row['uptime']) if uptime_row else 'Unknown'
            
            lag_val = '0ms'
            rep_stat = await conn.fetchrow("SELECT COALESCE(extract(epoch FROM (now() - pg_last_xact_replay_timestamp())) * 1000, 0) as lag_ms")
            if rep_stat and rep_stat['lag_ms'] > 0:
                lag_val = f"{int(rep_stat['lag_ms'])}ms"
                
            plates_count = 'N/A'
            try:
                plate_row = await conn.fetchrow("SELECT count(*) as count FROM vehicles")
                if plate_row:
                    plates_count = f"{plate_row['count']} Araç"
            except Exception:
                pass
            
            return {
                'status': 'online',
                'ping': f'{ping_ms}ms',
                'storage': f'{int(db_size_kb)} kB',
                'connections': f'{active_conn} / {max_conn}',
                'cache_hit': f'{cache_hit:.1f}%',
                'xact': f'{commits} ✔ / {rollbacks} ✖',
                'version': version_str,
                'uptime': uptime,
                'lag': lag_val,
                'plates': plates_count
            }
        finally:
            await conn.close()
    except Exception as e:
        return {'status': 'offline', 'error': str(e)}
