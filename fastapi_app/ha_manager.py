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
                await asyncio.to_thread(sync_schema_between_dbs, project_id, primary_url, s['url'], replication_tables, check_lease_cb)
            except Exception as schema_err:
                print(f"Schema sync error: {schema_err}")
                return {"success": False, "message": f"Schema sync failed: {str(schema_err)}"}

        # 2. Setup Primary (Idempotent)
        if check_lease_cb: check_lease_cb()
        p_conn = await asyncpg.connect(primary_url, timeout=10.0)
        lock_acquired_p = False
        try:
            has_lock = await p_conn.fetchval("SELECT pg_try_advisory_lock($1)", project_id)
            if not has_lock:
                return {"success": False, "message": "Could not acquire advisory lock on primary for publication."}
            lock_acquired_p = True
                
            # Check if publication exists
            pub_exists = await p_conn.fetchval(f"SELECT pubname FROM pg_publication WHERE pubname = 'univ_pub_{project_id}';")
            if pub_exists:
                if check_lease_cb: check_lease_cb()
                await p_conn.execute(f"ALTER PUBLICATION univ_pub_{project_id} SET TABLE {safe_tables_str};")
            else:
                if check_lease_cb: check_lease_cb()
                await p_conn.execute(f"CREATE PUBLICATION univ_pub_{project_id} FOR TABLE {safe_tables_str};")
        except Exception as pub_err:
            return {"success": False, "message": f"Failed to configure primary publication: {pub_err}"}
        finally:
            if not p_conn.is_closed():
                if lock_acquired_p:
                    try:
                        await p_conn.execute("SELECT pg_advisory_unlock($1)", project_id)
                    except:
                        pass
                await p_conn.close()

        # 3. Setup Standbys (Idempotent)
        if state_callback:
            await state_callback("CATCHING_UP")
        
        safe_primary_url = primary_url.replace("'", "''")
        
        for s in valid_standbys:
            if check_lease_cb: check_lease_cb()
            try:
                s_conn = await asyncpg.connect(s['url'], timeout=10.0, command_timeout=30.0, server_settings={'statement_timeout': '30000', 'lock_timeout': '10000'})
                lock_acquired_s = False
                try:
                    has_lock = await s_conn.fetchval("SELECT pg_try_advisory_lock($1)", project_id)
                    if not has_lock:
                        return {"success": False, "message": f"Could not acquire advisory lock on standby {s['id']}"}
                    lock_acquired_s = True
                        
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
                        if check_lease_cb: check_lease_cb()
                        await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} SET PUBLICATION univ_pub_{project_id};")
                        if check_lease_cb: check_lease_cb()
                        await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} ENABLE;")
                        if check_lease_cb: check_lease_cb()
                        await s_conn.execute(f"ALTER SUBSCRIPTION {sub_name} REFRESH PUBLICATION;")
                finally:
                    if not s_conn.is_closed():
                        if lock_acquired_s:
                            try:
                                await s_conn.execute("SELECT pg_advisory_unlock($1)", project_id)
                            except:
                                pass
                        await s_conn.close()
            except Exception as sub_err:
                return {"success": False, "message": f"Failed to configure standby subscription {s['id']}: {sub_err}"}

        return {"success": True, "message": f"Logical replication (1 Master to {len(valid_standbys)} Standbys) established safely."}

    except Exception as e:
        print(f"Replication setup error: {e}")
        return {"success": False, "message": f"Setup failed: {str(e)}"}


def sync_schema_between_dbs(project_id: int, primary_url: str, standby_url: str, replication_tables: str = None, check_lease_cb=None):
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

    from sqlalchemy import create_engine, MetaData, text
    engine_primary = create_engine(p_url, connect_args={"connect_timeout": 10})
    engine_standby = create_engine(s_url, connect_args={"connect_timeout": 10})

    with engine_primary.connect() as conn_p, engine_standby.connect() as conn_s:
        # Advisory locks via sync driver
        has_lock_p = conn_p.execute(text("SELECT pg_try_advisory_lock(:id)"), {"id": project_id}).scalar()
        if not has_lock_p:
            raise RuntimeError(f"Could not acquire advisory lock on primary for project {project_id}")
            
        has_lock_s = conn_s.execute(text("SELECT pg_try_advisory_lock(:id)"), {"id": project_id}).scalar()
        if not has_lock_s:
            conn_p.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": project_id})
            raise RuntimeError(f"Could not acquire advisory lock on standby for project {project_id}")
            
        try:
            if check_lease_cb: check_lease_cb()
            metadata = MetaData()
            # Primary'den sadece belirtilen tablo yapılarını oku
            metadata.reflect(bind=conn_p, only=tables_to_sync)
            
            if check_lease_cb: check_lease_cb()
            # Standby'da aynı tabloları yarat (Var olanları atlar - checkfirst=True varsayılandır)
            metadata.create_all(bind=conn_s)
            print(f"Schema sync completed. Processed {len(metadata.tables)} tables.")
        finally:
            try:
                conn_p.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": project_id})
            except:
                pass
            try:
                conn_s.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": project_id})
            except:
                pass

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

async def get_server_metrics(node: dict, project_id: int = None) -> dict:
    try:
        url = decrypt(node['encrypted_url'])
        role = node['role']
        metric_table = node.get('metric_table')
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
            
            stat_row = await conn.fetchrow('SELECT blks_hit, blks_read, xact_commit, xact_rollback, tup_fetched, tup_inserted, tup_updated, tup_deleted FROM pg_stat_database WHERE datname = current_database()')
            if stat_row:
                total_blks = (stat_row['blks_hit'] or 0) + (stat_row['blks_read'] or 0)
                cache_hit = (stat_row['blks_hit'] / total_blks * 100) if total_blks > 0 else 100.0
                commits = stat_row['xact_commit'] or 0
                rollbacks = stat_row['xact_rollback'] or 0
                tup_fetched = stat_row['tup_fetched'] or 0
                tup_inserted = stat_row['tup_inserted'] or 0
                tup_updated = stat_row['tup_updated'] or 0
                tup_deleted = stat_row['tup_deleted'] or 0
            else:
                cache_hit, commits, rollbacks = 100.0, 0, 0
                tup_fetched, tup_inserted, tup_updated, tup_deleted = 0, 0, 0, 0
                
            ver_row = await conn.fetchrow('SELECT version()')
            version_str = ver_row['version'].split('on')[0].strip() if ver_row else 'Unknown'
            
            uptime_row = await conn.fetchrow("SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime")
            raw_uptime = str(uptime_row['uptime']) if uptime_row else 'Unknown'
            uptime = raw_uptime.replace('days', 'gün').replace('day', 'gün')
            
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
            
            
            # Fetch OS metrics via SSH if available
            os_metrics = {'cpu': 'N/A', 'ram': 'N/A'}
            if node.get('ssh_host') and node.get('encrypted_ssh_credential'):
                import asyncio
                
                def fetch_os():
                    from ssh_worker import SSHManager
                    ssh_cred = decrypt(node['encrypted_ssh_credential'])
                    if not ssh_cred: return {}
                    try:
                        with SSHManager(node['ssh_host'], node.get('ssh_port', 22), node.get('ssh_username', 'root'), ssh_cred) as ssh:
                            # Basic Linux commands for CPU and RAM
                            cpu_out, _, _ = ssh.execute_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
                            ram_out, _, _ = ssh.execute_command("free -m | awk 'NR==2{printf \"%.1f\", $3*100/$2 }'")
                            
                            cpu = cpu_out.strip()
                            ram = ram_out.strip()
                            return {'cpu': f"{cpu}%" if cpu else 'N/A', 'ram': f"{ram}%" if ram else 'N/A'}
                    except Exception as e:
                        print("SSH Metric error:", e)
                        return {}
                
                try:
                    os_res = await asyncio.to_thread(fetch_os)
                    os_metrics.update(os_res)
                except:
                    pass

            return {
                'status': 'online',
                'ping': f"{int(ping_ms)}ms",
                'storage': f'{db_size_kb/1024:.1f} MB' if db_size_kb > 1024 else f'{int(db_size_kb)} kB',
                'connections': f'{active_conn} / {max_conn}',
                'cache_hit': f'{cache_hit:.1f}%',
                'xact': f'{commits:,} ✓ / {rollbacks:,} ✗',
                'version': version_str,
                'uptime': uptime,
                'lag': lag_val,
                'plates': plates_count,
                  'row_count': plates_count,
                'active_conn': active_conn,
                'max_conn': max_conn,
                'cache_hit_raw': cache_hit,
                'commits_raw': commits,
                'rollbacks_raw': rollbacks,
                'tup_fetched': tup_fetched,
                'tup_inserted': tup_inserted,
                'tup_updated': tup_updated,
                'tup_deleted': tup_deleted,
                'cpu_usage': os_metrics.get('cpu', 'N/A'),
                'ram_usage': os_metrics.get('ram', 'N/A')
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

