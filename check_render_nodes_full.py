with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('window.renderNodesPage = function() {')
idx_end = js.find('window.filterNodes = function', idx)
print(js[idx:idx_end].encode('ascii', errors='replace').decode('ascii'))
