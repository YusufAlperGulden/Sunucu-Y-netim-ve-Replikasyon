with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderNodesPage()')
idx2 = js.find('// Update stats', idx)
if idx2 == -1:
    idx2 = js.find('function filterNodes', idx)
if idx2 == -1:
    idx2 = idx + 4000
print(js[idx+2000:idx2+500].encode('ascii', errors='replace').decode('ascii'))
