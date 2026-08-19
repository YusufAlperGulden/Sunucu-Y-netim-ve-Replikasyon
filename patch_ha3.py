with open("fastapi_app/ha_manager.py", "r", encoding="utf-8") as f:
    content = f.read()

old_str = """                'plates': plates_count
            }
        finally:"""

new_str = """                'plates': plates_count,
                'active_conn': active_conn,
                'max_conn': max_conn,
                'cache_hit_raw': cache_hit,
                'commits_raw': commits,
                'rollbacks_raw': rollbacks,
                'tup_fetched': tup_fetched,
                'tup_inserted': tup_inserted,
                'tup_updated': tup_updated,
                'tup_deleted': tup_deleted
            }
        finally:"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open("fastapi_app/ha_manager.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched.")
else:
    print("Not found.")
