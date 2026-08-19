with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderNodesPage()')
idx_end = js.find('// --- API CALLS ---', idx)
if idx_end == -1:
    idx_end = idx + 3000
print(js[idx:idx_end].encode('ascii', errors='replace').decode('ascii'))
