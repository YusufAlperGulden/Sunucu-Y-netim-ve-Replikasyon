with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('async function fetchDashboardMetrics()')
print(js[idx+1800:idx+4000].encode('ascii', errors='replace').decode('ascii'))
