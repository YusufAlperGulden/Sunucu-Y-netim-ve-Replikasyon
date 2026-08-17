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

async def setup_replication(project_id: int, primary_encrypted_url: str, standbys_info: list, replication_tables: str = None, state_callback=None) -> dict:
    """İki veya daha fazla sunucu arasında PUBLICATION ve SUBSCRIPTION tünellerini (Logical Replication) kurar."""
    try:
        primary_url = decrypt(primary_encrypted_url)
        
        valid_standbys = []
        for s_info in standbys_info:
            dec = decrypt(s_info['url'])
            if dec:
                valid_standbys.append({'id': s_info['id'], 'url': dec})
                
        if not primary_url or not valid_standbys:
            return {"success": False, "message": "Failed to decrypt URLs or no valid standbys"}

        if state_callback:
            await state_callback("BOOTSTRAPPING")

        for s in valid_standbys:
            try:
                await asyncio.to_thread(sync_schema_between_dbs, primary_url, s['url'], replication_tables)
            except Exception as schema_err:
                print(f"Schema sync error: {schema_err}")
                return {"success": False, "message": f"Schema sync failed: {str(schema_err)}"}

        for s in valid_standbys:
            try:
                s_conn = await asyncpg.connect(s['url'], timeout=10.0)
                sub_name = f"univ_sub_{project_id}_{s['id']}"
                await s_conn.execute(f"DROP SUBSCRIPTION IF EXISTS {sub_name};")
                await s_conn.close()
            except Exception as e:
                print(f"Standby {s['id']} drop subscription error: {e}")

        # 2. Primary Sunucuya Bağlan, PUBLICATION oluştur ve eski Slotları tamamen temizle
        p_conn = await asyncpg.connect(primary_url, timeout=10.0)
        try:
            await p_conn.execute(f"DROP PUBLICATION IF EXISTS univ_pub_{project_id};")
            if not replication_tables:
                raise ValueError("CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety.")
            
            tables_list = [t.strip() for t in replication_tables.split(",") if t.strip()]
            if not tables_list:
                raise ValueError("CRITICAL: replication_tables must be provided. Syncing all tables is disabled for safety.")
                
            safe_tables = []
            for t in tables_list:
                if not re.match(r'^[a-zA-Z0-9_]+$', t):
                    raise ValueError(f"Invalid table name detected: {t}")
                safe_tables.append(f'"{t}"')
                
            safe_tables_str = ", ".join(safe_tables)
            await p_conn.execute(f"CREATE PUBLICATION univ_pub_{project_id} FOR TABLE {safe_tables_str};")
            
            # Primary'deki tüm 'universal_sub' ile başlayan slotları bul ve zorla sil
            slots = await p_conn.fetch(f"SELECT slot_name, active_pid FROM pg_replication_slots WHERE slot_name LIKE 'univ_sub_{project_id}_%';")
            for slot in slots:
                slot_name = slot['slot_name']
                active_pid = slot['active_pid']
                try:
                    if active_pid:
                        await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")
                    await p_conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")
                    print(f"Dropped orphaned slot: {slot_name}")
                except Exception as e:
                    print(f"Could not drop slot {slot_name}: {e}")
        finally:
            await p_conn.close()

        # 4. Standby Sunuculara Bağlan, SUBSCRIPTION oluştur
        if state_callback:
            await state_callback("CATCHING_UP")
        
        # 3. Tüm Standby Sunuculara tekrar Bağlan ve YENİ SUBSCRIPTION oluştur
        safe_primary_url = primary_url.replace("'", "''")
        created_subs = []
        try:
            for s in valid_standbys:
                s_conn = await asyncpg.connect(s['url'], timeout=10.0)
                try:
                    sub_name = f"univ_sub_{project_id}_{s['id']}"
                    sub_query = f"CREATE SUBSCRIPTION {sub_name} CONNECTION '{safe_primary_url}' PUBLICATION univ_pub_{project_id} WITH (copy_data = true);"
                    await s_conn.execute(sub_query)
                    created_subs.append((s['url'], sub_name))
                finally:
                    await s_conn.close()
        except Exception as setup_err:
            print(f"Standby setup failed, rolling back previously created subs. Error: {setup_err}")
            rollback_failed = False
            rollback_errors = []
            
            for roll_url, roll_sub in created_subs:
                try:
                    r_conn = await asyncpg.connect(roll_url, timeout=5.0)
                    await r_conn.execute(f"ALTER SUBSCRIPTION {roll_sub} DISABLE;")
                    await r_conn.execute(f"ALTER SUBSCRIPTION {roll_sub} SET (slot_name = NONE);")
                    await r_conn.execute(f"DROP SUBSCRIPTION IF EXISTS {roll_sub};")
                    await r_conn.close()
                except Exception as rollback_err:
                    print(f"Failed to rollback sub {roll_sub}: {rollback_err}")
                    rollback_failed = True
                    rollback_errors.append(str(rollback_err))
                    
            try:
                p_conn = await asyncpg.connect(primary_url, timeout=5.0)
                for _, roll_sub in created_subs:
                    try:
                        active_pid = await p_conn.fetchval(f"SELECT active_pid FROM pg_replication_slots WHERE slot_name = '{roll_sub}';")
                        if active_pid:
                            await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")
                        await p_conn.execute(f"SELECT pg_drop_replication_slot('{roll_sub}');")
                    except Exception as primary_roll_err:
                        print(f"Failed to drop replication slot {roll_sub}: {primary_roll_err}")
                        rollback_failed = True
                        rollback_errors.append(str(primary_roll_err))
                        
                try:
                    await p_conn.execute(f"DROP PUBLICATION IF EXISTS univ_pub_{project_id};")
                except Exception as pub_roll_err:
                    print(f"Failed to drop publication: {pub_roll_err}")
                    rollback_failed = True
                    rollback_errors.append(str(pub_roll_err))
                await p_conn.close()
            except Exception as p_conn_err:
                rollback_failed = True
                rollback_errors.append(str(p_conn_err))
                
            if rollback_failed:
                return {"success": False, "message": f"ROLLBACK_FAILED: Setup failed with '{setup_err}', AND rollback also failed: {', '.join(rollback_errors)}"}
            return {"success": False, "message": f"Standby setup failed, but rolled back successfully. Error: {setup_err}"}

        return {"success": True, "message": f"Logical replication (1 Master to {len(valid_standbys)} Standbys) established successfully."}

    except Exception as e:
        print(f"Replication setup error: {e}")
        return {"success": False, "message": f"Setup failed: {str(e)}"}

def sync_schema_between_dbs(primary_url: str, standby_url: str, replication_tables: str = None):
    """SQLAlchemy MetaData Reflection kullanarak şemaları kopyalar (Sadece iskelet)."""
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

    metadata = MetaData()
    # Primary'den sadece belirtilen tablo yapılarını oku
    metadata.reflect(bind=engine_primary, only=tables_to_sync)
    
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
                subs = await conn.fetch(f"SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes FROM pg_replication_slots WHERE slot_name LIKE 'univ_sub_{project_id}_%' ORDER BY lag_bytes DESC LIMIT 1;")
                if subs and len(subs) > 0 and subs[0]['lag_bytes'] is not None:
                    lag_mb = subs[0]['lag_bytes'] / (1024 * 1024)
                    lag_val = f"{lag_mb:.2f} MB"
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
async def run_sync_state_machine_bg(project_id: int):
    from models import SessionLocal, Project, AuditLog
    import asyncio
    db = SessionLocal()
    
    try:
        proj = db.query(Project).filter(Project.id == project_id).first()
        if not proj:
            return
            
        async def state_callback(state: str):
            # Yeniden sorgulama yapmak iyi olabilir
            p = db.query(Project).filter(Project.id == project_id).first()
            if p:
                p.sync_status = state
                db.commit()

        # VALIDATING
        await state_callback("VALIDATING")
        primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
        standbys = [n for n in proj.nodes if n.role.lower() == 'standby']
        
        if not primary or not standbys:
            proj.sync_status = "FAILED"
            proj.sync_error = "Projenizde en az 1 Primary ve 1 Standby node bulunmalidir."
            proj.sync_locked_at = None
            db.commit()
            return
            
        standbys_info = [{"id": s.id, "url": s.encrypted_url} for s in standbys]
        result = await setup_replication(project_id, primary.encrypted_url, standbys_info, proj.replication_tables, state_callback)
        
        # Sonucu veritabanina yaz
        proj = db.query(Project).filter(Project.id == project_id).first()
        if result['success']:
            proj.sync_status = "HEALTHY"
            proj.sync_error = ""
            audit = AuditLog(project_id=project_id, action="Replication Synced", details="Background Sync Job completed successfully.")
            db.add(audit)
        else:
            if "ROLLBACK_FAILED" in result.get('message', ''):
                proj.sync_status = "ROLLBACK_FAILED"
            else:
                proj.sync_status = "FAILED"
            proj.sync_error = result.get('message', 'Unknown Error')
            audit = AuditLog(project_id=project_id, action="Sync Failed", details=proj.sync_error)
            db.add(audit)
            
        proj.sync_locked_at = None
        db.commit()
    except Exception as e:
        proj = db.query(Project).filter(Project.id == project_id).first()
        if proj:
            proj.sync_status = "FAILED"
            proj.sync_error = str(e)
            proj.sync_locked_at = None
            db.commit()
    finally:
        db.close()
