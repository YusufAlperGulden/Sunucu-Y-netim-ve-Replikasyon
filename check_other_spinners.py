with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's check fetchBackups and renderReports
for fn in ['renderReports', 'fetchUsers', 'fetchBackups', 'fetchProjects']:
    idx = js.find(fn)
    if idx != -1:
        print(f"--- {fn} ---")
        print(js[idx:idx+400].encode('ascii', errors='replace').decode('ascii'))
