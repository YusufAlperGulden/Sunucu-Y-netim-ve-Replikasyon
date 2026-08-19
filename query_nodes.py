import sqlite3
import json

db_file = 'fastapi_app.db'
try:
    conn = sqlite3.connect(f'fastapi_app/{db_file}')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM nodes;")
    rows = c.fetchall()
    print("Nodes:")
    for row in rows:
        print(dict(row))
    c.execute("SELECT * FROM projects;")
    rows = c.fetchall()
    print("Projects:")
    for row in rows:
        print(dict(row))
    conn.close()
except Exception as e:
    print(f"Error: {e}")
