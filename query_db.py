import sqlite3

for db_file in ['fastapi_app.db', 'univ.db', 'projects.db', 'test.db']:
    try:
        conn = sqlite3.connect(f'fastapi_app/{db_file}')
        c = conn.cursor()
        c.execute("SELECT host, ip_address, role, project_id, type FROM database_node;")
        rows = c.fetchall()
        print(f"Data from {db_file}:")
        for row in rows:
            print(row)
        conn.close()
    except Exception as e:
        print(f"Could not read {db_file}: {e}")
