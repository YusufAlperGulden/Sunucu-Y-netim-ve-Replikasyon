import asyncpg
import asyncio
import re
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

async def setup_replication(project_id: int, primary_encrypted_url: str, standbys_info: list, replication_tables: str = None, state_callback=None, check_lease_cb=None) -> dict:
    try:
        primary_url = decrypt(primary_encrypted_url)
        
        valid_standbys = []
        for s_info in standbys_info:
            dec = decrypt(s_info['url'])
            if dec:
                valid_standbys.append({'id': s_info['id'], 'url': dec})
                
        if not primary_url or not valid_standbys:
            return {"success": False, "message": "Failed to decrypt URLs or no valid standbys"}

        if not replication_tables:
            return {"success": False, "message": "CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety."}
            
        tables_list = [t.strip() for t in replication_tables.split(",") if t.strip()]
        if not tables_list:
            return {"success": False, "message": "CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety."}

        safe_tables = []
        for t in tables_list:
            if not re.match(r'^[a-zA-Z0-9_]+$', t):
                return {"success": False, "message": f"Invalid table name detected: {t}"}
            safe_tables.append(f'"{t}"')
            
        safe_tables_str = ", ".join(safe_tables)

        # PREFLIGHT CHECKS
        try:
            p_conn = await asyncpg.connect(primary_url, timeout=10.0)
            
            # Check wal_level
            wal_level = await p_conn.fetchval("SHOW wal_level;")
            if wal_level != 'logical':
                await p_conn.close()
                return {"success": False, "message": f"Primary server wal_level is '{wal_level}', but must be 'logical'."}
            
            # Check table existence and Replica Identity
            for t in tables_list:
                exists = await p_conn.fetchval("SELECT to_regclass($1);", t)
                if not exists:
                    await p_conn.close()
                    return {"success": False, "message": f"Table '{t}' does not exist on primary server."}
                    
                repl_check = await p_conn.fetchrow("""
                    SELECT c.relreplident, 
                           (SELECT count(*) FROM pg_index i WHERE i.indrelid = c.oid AND i.indisprimary) as pk_count
                    FROM pg_class c
                    WHERE c.oid = $1::regclass;
                """, t)
                
                if repl_check:
                    if repl_check['relreplident'] == 'n':
                        await p_conn.close()
                        return {"success": False, "message": f"Table '{t}' has REPLICA IDENTITY NOTHING. Logical replication will crash on UPDATE/DELETE."}
                    if repl_check['relreplident'] == 'd' and repl_check['pk_count'] == 0:
                        await p_conn.close()
                        return {"success": False, "message": f"Table '{t}' has no Primary Key and default REPLICA IDENTITY. Logical replication will crash on UPDATE/DELETE."}
                    
            await p_conn.close()
        except Exception as preflight_err:
            return {"success": False, "message": f"Preflight validation failed on primary: {preflight_err}"}

        # Standby Connection Tests
        for s in valid_standbys:
            try:
                s_conn = await asyncpg.connect(s['url'], timeout=10.0)
                await s_conn.close()
            except Exception as e:
                return {"success": False, "message": f"Preflight validation failed on standby {s['id']}: {e}"}

        # ACTUAL SETUP (Idempotent)
        if state_callback:
            await state_callback("BOOTSTRAPPING")

        # 1. Sync Schemas
        for s in valid_standbys:
            try:
                if check_lease_cb: check_lease_cb()
                await asyncio.to_thread(sync_schema_between_dbs, primary_url, s['url'], replication_tables, check_lease_cb)
            except Exception as schema_err:
                print(f"Schema sync error: {schema_err}")
                return {"success": False, "message": f"Schema sync failed: {str(schema_err)}"}

        # 2. Setup Primary (Idempotent)
        if check_lease_cb: check_lease_cb()
        p_conn = await asyncpg.connect(primary_url, timeout=10.0)
        try:
            # Check if publication exists
            pub_exists = await p_conn.fetchval(f"SELECT pubname FROM pg_publication WHERE pubname = 'univ_pub_{project_id}';")
            if pub_exists:
                # Alter publication to add/remove tables
                await p_conn.execute(f"ALTER PUBLICATION univ_pub_{project_id} SET TABLE {safe_tables_str};")
            else:
                await p_conn.execute(f"CREATE PUBLICATION univ_pub_{project_id} FOR TABLE {safe_tables_str};")
        except Exception as pub_err:
            await p_conn.close()
            return {"success": False, "message": f"Failed to configure primary publication: {pub_err}"}
        
        await p_conn.close()

        # 3. Setup Standbys (Idempotent)
        if state_callback:
            await state_callback("CATCHING_UP")
        
        safe_primary_url = primary_url.replace("'", "''")
        
        for s in valid_standbys:
            if check_lease_cb: check_lease_cb()
            try:
                s_conn = await asyncpg.connect(s['url'], timeout=10.0)
                sub_name = f"univ_sub_{project_id}_{s['id']}"
                
                # Check if subscription exists
                sub_exists = await s_conn.fetchval(f"SELECT subname FROM pg_subscription WHERE subname = '{sub_name}';")
                if not sub_exists:
                    if check_lease_cb: check_lease_cb()
                    sub_query = f"CREATE SUBSCRIPTION {sub_name} CONNECTION '{safe_primary_url}' PUBLICATION univ_pub_{project_id} WITH (copy_data = true);"
                    await s_conn.execute(sub_query)
                else:
                    # Force the connection, publication, and enable state
                    if check_lease_cb: check_lease_cb()
                    await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} CONNECTION '{safe_primary_url}';")
                    await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} SET PUBLICATION univ_pub_{project_id};")
                    await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} ENABLE;")
                    await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} REFRESH PUBLICATION;")
                    
                await s_conn.close()
            except Exception as sub_err:
                return {"success": False, "message": f"Failed to configure standby subscription {sub_name}: {sub_err}"}

        return {"success": True, "message": f"Logical replication (1 Master to {len(valid_standbys)} Standbys) established safely."}

    except Exception as e:
        print(f"Replication setup error: {e}")
        return {"success": False, "message": f"Setup failed: {str(e)}"}


def sync_schema_between_dbs(primary_url: str, standby_url: str, replication_tables: str = None, check_lease_cb=None):
    """SQLAlchemy MetaData Reflection kullanarak şemaları kopyalar (Sadece iskelet)."""
    if check_lease_cb: check_lease_cb()
    if not replication_tables:
        raise ValueError("CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety.")
        
    tables_to_sync = [t.strip() for t in replication_tables.split(",") if t.strip()]
    if not tables_to_sync:
        raise ValueError("CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety.")
        
    for t in tables_to_sync:
        if not re.match(r'^[a-zA-Z0-9_]+$', t):
            raise ValueError(f"Invalid table name detected: {t}")
            
    # asyncpg url (postgres://) ile sqlalchemy url (postgresql://) uyumu
    p_url = primary_url.replace("postgres://", "postgresql://")
    s_url = standby_url.replace("postgres://", "postgresql://")

    engine_primary = create_engine(p_url)
    engine_standby = create_engine(s_url)

    if check_lease_cb: check_lease_cb()
    metadata = MetaData()
    # Primary'den sadece belirtilen tablo yapılarını oku
    metadata.reflect(bind=engine_primary, only=tables_to_sync)
    
    if check_lease_cb: check_lease_cb()
    # Standby'da aynı tabloları yarat (Var olanları atlar - checkfirst=True varsayılandır)
    metadata.create_all(bind=engine_standby)
    print(f"Schema sync completed. Processed {len(metadata.tables)} tables.")

async def check_and_protect_wal_bloat(project_id: int, primary_encrypted_url: str, max_wal_lag_mb: int) -> dict:
    """Primary sunucuya bağlanarak WAL lag'i ölçer. Kritik seviyeyi aşarsa slot'u koparır."""
    try:
        primary_url = decrypt(primary_encrypted_url)
        if not primary_url:
            return {"success": False, "message": "Failed to decrypt URL", "dropped": False}

        conn = await asyncpg.connect(primary_url, timeout=5.0)
        try:
            # Replikasyon gecikmesini byte cinsinden hesaplayan PostgreSQL sorgusu
            # universal_sub adlı subscription için universal_sub slotu oluşuyor
            query = f"""
                SELECT slot_name, 
                       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes 
                FROM pg_replication_slots 
                WHERE slot_name LIKE 'univ_sub_{project_id}_%';
            """
            rows = await conn.fetch(query)
            
            if not rows:
                return {"success": True, "message": "No active replication slots found.", "dropped": False, "lag_mb": 0}
            
            max_lag_mb = 0
            dropped_slots = []
            for row in rows:
                if row['lag_bytes'] is None:
                    continue
                lag_mb = row['lag_bytes'] / (1024 * 1024)
                max_lag_mb = max(max_lag_mb, lag_mb)
                
                # Kritik eşiği aştı mı?
                if lag_mb > max_wal_lag_mb:
                    slot_name = row['slot_name']
                    print(f"[CRITICAL] WAL lag ({lag_mb:.2f} MB) exceeded max limit for {slot_name}. Dropping slot!")
                    # Terminate active backend first if active
                    active_pid_row = await conn.fetchrow(f"SELECT active_pid FROM pg_replication_slots WHERE slot_name='{slot_name}';")
                    if active_pid_row and active_pid_row['active_pid']:
                        await conn.execute(f"SELECT pg_terminate_backend({active_pid_row['active_pid']});")
                    await conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")
                    dropped_slots.append(slot_name)
                    
            if dropped_slots:
                return {"success": True, "message": f"CRITICAL: Dropped slots {dropped_slots} to prevent WAL bloat.", "dropped": True, "lag_mb": max_lag_mb}
            else:
                return {"success": True, "message": f"Lag is healthy (Max {max_lag_mb:.2f} MB)", "dropped": False, "lag_mb": max_lag_mb}
                
        finally:
            await conn.close()

    except Exception as e:
        print(f"WAL Bloat check error: {e}")
        return {"success": False, "message": f"Check failed: {str(e)}", "dropped": False, "lag_mb": 0}

import time

async def get_server_metrics(encrypted_url: str, project_id: int = None, role: str = None, metric_table: str = None) -> dict:
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
            
            lag_val = 'Bağlantı Bekleniyor'
            # Check replication lag
            if role and role.lower() == 'primary' and project_id:
                try:
                    ver_num = await conn.fetchval("SELECT current_setting('server_version_num')::int")
                    invalidation_col = "invalidation_reason" if ver_num >= 170000 else "NULL as invalidation_reason"
                except:
                    invalidation_col = "NULL as invalidation_reason"

                query = f"""
                    SELECT slot_name, active, wal_status, {invalidation_col},
                           pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn) AS consumer_gap_bytes,
                           pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS retained_wal_bytes
                    FROM pg_replication_slots
                    WHERE slot_type = 'logical' AND database = current_database();
                """
                slots = await conn.fetch(query)
                proj_slots = [s for s in slots if s['slot_name'].startswith(f'univ_sub_{project_id}_')]
                if proj_slots:
                    s = proj_slots[0]
                    active = s['active']
                    wal_status = s['wal_status']
                    inv_reason = s['invalidation_reason']
                    gap_mb = (s['consumer_gap_bytes'] / (1024*1024)) if s['consumer_gap_bytes'] is not None else 0
                    retained_mb = (s['retained_wal_bytes'] / (1024*1024)) if s['retained_wal_bytes'] is not None else 0
                    if inv_reason is not None or wal_status == 'lost':
                        lag_val = f"LOST (Neden: {inv_reason or wal_status})"
                    elif not active:
                        lag_val = f"DISCONNECTED (Biriken WAL: {retained_mb:.1f} MB)"
                    else:
                        lag_val = f"STREAMING (Gap: {gap_mb:.2f} MB)"
                else:
                    if slots:
                        lag_val = "Legacy/Harici Replikasyon Algılandı"
                    else:
                        lag_val = "Konfigüre Edilmedi (NOT_CONFIGURED)"
            elif role and role.lower() == 'standby':
                lag_val = 'Subscriber'
            else:
                lag_val = 'N/A' 
                
            plates_count = 'Metrik Ayarlanmadı'
            if metric_table:
                try:
                    count_row = await conn.fetchrow(f'SELECT count(*) as count FROM "{metric_table}"')
                    if count_row:
                        plates_count = f"{count_row['count']} Kayıt ({metric_table})"
                except Exception:
                    plates_count = f"Tablo Bulunamadı ({metric_table})"
            
            return {
                'status': 'online',
                'ping': f"{int(ping_ms)}ms",
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


async def cleanup_node_replication(project_id: int, node_id: int, primary_url: str, standby_url: str = None):
    sub_name = f"univ_sub_{project_id}_{node_id}"
    # 1. Drop sub on standby first
    if standby_url:
        try:
            s_conn = await asyncpg.connect(standby_url, timeout=5.0)
            sub_exists = await s_conn.fetchrow(f"SELECT 1 FROM pg_subscription WHERE subname='{sub_name}';")
            if sub_exists:
                await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} DISABLE;")
                await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} SET (slot_name = NONE);")
                await s_conn.execute(f"DROP SUBSCRIPTION IF EXISTS {sub_name};")
            await s_conn.close()
        except Exception as e:
            print(f"Cleanup node sub err: {e}")
            raise Exception(f"Standby cleanup failed: {e}")
            
    # 2. Drop slot on primary
    try:
        p_conn = await asyncpg.connect(primary_url, timeout=5.0)
        active_pid_row = await p_conn.fetchrow(f"SELECT active_pid FROM pg_replication_slots WHERE slot_name='{sub_name}';")
        if active_pid_row:
            if active_pid_row['active_pid']:
                await p_conn.execute(f"SELECT pg_terminate_backend({active_pid_row['active_pid']});")
            await p_conn.execute(f"SELECT pg_drop_replication_slot('{sub_name}');")
        await p_conn.close()
    except Exception as e:
        print(f"Cleanup node slot err: {e}")
        # Only raise if it's not a 'does not exist' error
        if "does not exist" not in str(e):
            raise Exception(f"Primary cleanup failed: {e}")

async def cleanup_project_replication(project_id: int, primary_url: str, standby_urls: list):
    # Drop subscriptions first
    for s_url in standby_urls:
        try:
            s_conn = await asyncpg.connect(s_url, timeout=5.0)
            subs = await s_conn.fetch(f"SELECT subname FROM pg_subscription WHERE subname LIKE 'univ_sub_{project_id}_%';")
            for sub in subs:
                await s_conn.execute(f"ALTER SUBSCRIPTION {sub['subname']} DISABLE;")
                await s_conn.execute(f"ALTER SUBSCRIPTION {sub['subname']} SET (slot_name = NONE);")
                await s_conn.execute(f"DROP SUBSCRIPTION IF EXISTS {sub['subname']};")
            await s_conn.close()
        except Exception as e:
            print(f"Cleanup proj sub err: {e}")
            raise Exception(f"Standby {s_url} cleanup failed: {e}")
            
    # Then primary
    try:
        p_conn = await asyncpg.connect(primary_url, timeout=5.0)
        slots = await p_conn.fetch(f"SELECT slot_name, active_pid FROM pg_replication_slots WHERE slot_name LIKE 'univ_sub_{project_id}_%';")
        for slot in slots:
            slot_name = slot['slot_name']
            active_pid = slot['active_pid']
            if active_pid:
                await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")
            await p_conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")
            
        await p_conn.execute(f"DROP PUBLICATION IF EXISTS univ_pub_{project_id};")
        await p_conn.close()
    except Exception as e:
        print(f"Cleanup proj pub/slot err: {e}")
        raise Exception(f"Primary cleanup failed: {e}")

