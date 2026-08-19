with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('async function fetchDashboardMetrics()')
print(js[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
