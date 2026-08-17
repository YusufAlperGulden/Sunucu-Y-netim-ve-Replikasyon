with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace setup_replication signature
text = text.replace(
    'async def setup_replication(primary_encrypted_url: str, standby_encrypted_urls: list) -> dict:',
    'async def setup_replication(project_id: int, primary_encrypted_url: str, standby_encrypted_urls: list) -> dict:'
)

# Replace universal_sub/pub
text = text.replace('universal_sub_{idx}', 'univ_sub_{project_id}_{idx}')
text = text.replace('universal_sub;', 'univ_sub_{project_id}_{idx};')
text = text.replace('universal_pub', 'univ_pub_{project_id}')

# Fix the active_pid kill logic
bad_kill = 'await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")'
text = text.replace(bad_kill, '# Eliminated dangerous global pg_terminate_backend')

bad_kill_2 = 'await p_conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_replication;")'
text = text.replace(bad_kill_2, '# Eliminated dangerous global pg_terminate_backend')

# Fix slots query
text = text.replace("LIKE 'universal_sub%';", "LIKE f'univ_sub_{project_id}_%';")
text = text.replace("LIKE 'universal_sub%'", "LIKE f'univ_sub_{project_id}_%'")

# Replace check_and_protect_wal_bloat signature
text = text.replace(
    'async def check_and_protect_wal_bloat(primary_encrypted_url: str, max_wal_lag_mb: int) -> dict:',
    'async def check_and_protect_wal_bloat(project_id: int, primary_encrypted_url: str, max_wal_lag_mb: int) -> dict:'
)

# Fix the standby metric
standby_metric_bad = '''            # Check logical replication subscriptions
            subs = await conn.fetch("SELECT extract(epoch from (now() - last_msg_receipt_time))*1000 as lag_ms FROM pg_stat_subscription WHERE last_msg_receipt_time IS NOT NULL LIMIT 1;")
            if subs and len(subs) > 0 and subs[0]['lag_ms'] is not None:
                lag_val = f"{int(subs[0]['lag_ms'])}ms"
            else:
                # Eger Master ise N/A dondurebilir veya eger Standby ama mesaj gelmediyse 0 kabul edebilir
                pass'''

standby_metric_good = '''            # Check replication lag correctly
            subs = await conn.fetch("SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes FROM pg_stat_replication LIMIT 1;")
            if subs and len(subs) > 0 and subs[0]['lag_bytes'] is not None:
                lag_mb = subs[0]['lag_bytes'] / (1024 * 1024)
                lag_val = f"{lag_mb:.2f} MB"
            else:
                pass'''
text = text.replace(standby_metric_bad, standby_metric_good)

with open('fastapi_app/ha_manager.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
