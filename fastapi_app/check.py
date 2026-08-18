import sqlite3
conn = sqlite3.connect('univ.db')
print([x[0] for x in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
