import sqlite3

for db_file in ['univ.db', 'test.db', 'test_architecture.db']:
    try:
        conn = sqlite3.connect(f'fastapi_app/{db_file}')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM nodes;")
        rows = c.fetchall()
        if rows:
            print(f"Nodes in {db_file}:")
            for row in rows:
                print(dict(row))
        conn.close()
    except Exception as e:
        pass
