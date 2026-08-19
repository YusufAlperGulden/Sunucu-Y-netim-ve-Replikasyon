with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's check renderReports
idx = js.find('async function renderReports()')
if idx != -1:
    print(js[idx:idx+500].encode('ascii', errors='replace').decode('ascii'))
