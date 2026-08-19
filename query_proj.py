import sqlite3
try:
    conn = sqlite3.connect('fastapi_app/fastapi_app.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM projects;")
    for row in c.fetchall():
        print(dict(row))
    conn.close()
except Exception as e:
    print(f"Error: {e}")
