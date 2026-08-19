with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx_start = js.find('async function fetchDashboardMetrics()')
if idx_start == -1:
    idx_start = js.find('function fetchDashboardMetrics()')

idx_end = js.find('function startDashboardInterval()', idx_start)
if idx_end == -1:
    idx_end = js.find('// System Logs', idx_start)
if idx_end == -1:
    idx_end = js.find('window.openNewClusterModal', idx_start)

print("idx_start:", idx_start, "idx_end:", idx_end)
print(js[idx_start:idx_start+300].encode('ascii', errors='replace').decode('ascii'))
