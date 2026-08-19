with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

target = """            stat_row = await conn.fetchrow('SELECT blks_hit, blks_read, xact_commit, xact_rollback, tup_fetched, tup_inserted, tup_updated, tup_deleted FROM pg_stat_database WHERE datname = current_database()')
            if stat_row:
                total_blks = stat_row['blks_hit'] + stat_row['blks_read']
                cache_hit = (stat_row['blks_hit'] / total_blks * 100) if total_blks > 0 else 100.0
                commits = stat_row['xact_commit']
                rollbacks = stat_row['xact_rollback']
            else:
                cache_hit, commits, rollbacks = 100.0, 0, 0"""

replacement = """            stat_row = await conn.fetchrow('SELECT blks_hit, blks_read, xact_commit, xact_rollback, tup_fetched, tup_inserted, tup_updated, tup_deleted FROM pg_stat_database WHERE datname = current_database()')
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
                tup_fetched, tup_inserted, tup_updated, tup_deleted = 0, 0, 0, 0"""

if target in ha:
    ha = ha.replace(target, replacement, 1)
    with open('fastapi_app/ha_manager.py', 'w', encoding='utf-8') as f:
        f.write(ha)
    print("Successfully patched ha_manager.py")
else:
    print("Target block not found in ha_manager.py")
