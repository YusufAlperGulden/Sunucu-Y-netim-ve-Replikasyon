with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function fetchDashboardMetrics()')
if idx == -1:
    idx = js.find('async function fetchDashboardMetrics()')
print(js[idx:idx+3500].encode('ascii', errors='replace').decode('ascii'))
