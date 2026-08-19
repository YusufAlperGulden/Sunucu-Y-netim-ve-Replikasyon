import re
with open("fastapi_app/ha_manager.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the query for pg_stat_database
old_query = "'SELECT blks_hit, blks_read, xact_commit, xact_rollback FROM pg_stat_database WHERE datname = current_database()'"
new_query = "'SELECT blks_hit, blks_read, xact_commit, xact_rollback, tup_fetched, tup_inserted, tup_updated, tup_deleted FROM pg_stat_database WHERE datname = current_database()'"

content = content.replace(old_query, new_query)

# Now extract these fields
old_extract = """                if stat_row:
                    total_blks = stat_row['blks_hit'] + stat_row['blks_read']
                    cache_hit = (stat_row['blks_hit'] / total_blks * 100) if total_blks > 0 else 100.0
                    commits = stat_row['xact_commit']
                    rollbacks = stat_row['xact_rollback']
                else:
                    cache_hit, commits, rollbacks = 100.0, 0, 0"""

new_extract = """                if stat_row:
                    total_blks = stat_row['blks_hit'] + stat_row['blks_read']
                    cache_hit = (stat_row['blks_hit'] / total_blks * 100) if total_blks > 0 else 100.0
                    commits = stat_row['xact_commit']
                    rollbacks = stat_row['xact_rollback']
                    tup_fetched = stat_row['tup_fetched'] or 0
                    tup_inserted = stat_row['tup_inserted'] or 0
                    tup_updated = stat_row['tup_updated'] or 0
                    tup_deleted = stat_row['tup_deleted'] or 0
                else:
                    cache_hit, commits, rollbacks = 100.0, 0, 0
                    tup_fetched = tup_inserted = tup_updated = tup_deleted = 0"""
content = content.replace(old_extract, new_extract)

# And add them to the return dict
old_return = """                'transactions': f"{commits} \u2713 / {rollbacks} \u2717",
                'cache_hit': f"{cache_hit:.1f}%",
                'uptime': uptime_str,
                'version': version_str,
                'ping': f"{ping_ms}ms",
                'lag': "0ms",  # Mocked
                'storage': f"{int(db_size_kb)} kB",
                'connections': f"{active_conn} / {max_conn}"
            }"""

new_return = """                'transactions': f"{commits} \u2713 / {rollbacks} \u2717",
                'cache_hit': f"{cache_hit:.1f}%",
                'uptime': uptime_str,
                'version': version_str,
                'ping': f"{ping_ms}ms",
                'lag': "0ms",  # Mocked
                'storage': f"{int(db_size_kb)} kB",
                'connections': f"{active_conn} / {max_conn}",
                'active_conn': active_conn,
                'max_conn': max_conn,
                'cache_hit_raw': cache_hit,
                'commits_raw': commits,
                'rollbacks_raw': rollbacks,
                'tup_fetched': tup_fetched,
                'tup_inserted': tup_inserted,
                'tup_updated': tup_updated,
                'tup_deleted': tup_deleted
            }"""
content = content.replace(old_return, new_return)

with open("fastapi_app/ha_manager.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ha_manager.py")
