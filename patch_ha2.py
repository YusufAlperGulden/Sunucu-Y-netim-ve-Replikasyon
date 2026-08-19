import re

with open("fastapi_app/ha_manager.py", "r", encoding="utf-8") as f:
    content = f.read()

# I will find the exact return block and replace it using regex
return_pattern = re.compile(r"return \{\s*'status': 'online',\s*'cache_hit': f'\{cache_hit:\.1f\}%',\s*'xact': f'\{commits\}(.*?)/ \{rollbacks\}(.*?)',\s*'version': version_str,\s*'uptime': uptime,\s*'lag': lag_val,\s*'plates': plates_count\s*\}", re.DOTALL)

match = return_pattern.search(content)
if match:
    new_return = f"""return {{
                'status': 'online',
                'cache_hit': f'{{cache_hit:.1f}}%',
                'xact': f'{{commits}}{match.group(1)}/ {{rollbacks}}{match.group(2)}',
                'version': version_str,
                'uptime': uptime,
                'lag': lag_val,
                'plates': plates_count,
                'active_conn': active_conn,
                'max_conn': max_conn,
                'cache_hit_raw': cache_hit,
                'commits_raw': commits,
                'rollbacks_raw': rollbacks,
                'tup_fetched': tup_fetched,
                'tup_inserted': tup_inserted,
                'tup_updated': tup_updated,
                'tup_deleted': tup_deleted,
                'connections': f'{{active_conn}} / {{max_conn}}'
            }}"""
    content = content[:match.start()] + new_return + content[match.end():]
    
    with open("fastapi_app/ha_manager.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("ha_manager.py return patched successfully.")
else:
    print("Could not find the return block to patch.")
