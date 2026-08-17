with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'await p_conn.execute("DROP PUBLICATION IF EXISTS univ_pub_{project_id};")',
    'await p_conn.execute(f"DROP PUBLICATION IF EXISTS univ_pub_{project_id};")'
)

text = text.replace(
    'await p_conn.execute("CREATE PUBLICATION univ_pub_{project_id} FOR ALL TABLES;")',
    'await p_conn.execute(f"CREATE PUBLICATION univ_pub_{project_id} FOR ALL TABLES;")'
)

text = text.replace(
    'await s_conn.execute("DROP SUBSCRIPTION IF EXISTS univ_sub_{project_id}_{idx};")',
    'pass # old drop'
)

text = text.replace(
    'slots = await p_conn.fetch("SELECT slot_name, active_pid FROM pg_replication_slots WHERE slot_name LIKE f\'univ_sub_{project_id}_%\';")',
    'slots = await p_conn.fetch(f"SELECT slot_name, active_pid FROM pg_replication_slots WHERE slot_name LIKE \'univ_sub_{project_id}_%\';")'
)

text = text.replace(
    '''                try:
                    if active_pid:
                        # Eliminated dangerous global pg_terminate_backend
                    await p_conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")''',
    '''                try:
                    if active_pid:
                        await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")
                    await p_conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")'''
)

text = text.replace(
    '''            query = """
                SELECT slot_name, 
                       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes 
                FROM pg_replication_slots 
                WHERE slot_name LIKE f'univ_sub_{project_id}_%';
            """''',
    '''            query = f"""
                SELECT slot_name, 
                       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes 
                FROM pg_replication_slots 
                WHERE slot_name LIKE 'univ_sub_{project_id}_%';
            """'''
)

with open('fastapi_app/ha_manager.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done fixing syntax")
