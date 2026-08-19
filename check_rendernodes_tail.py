with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderNodesPage()')
print(js[idx+1600:idx+3200].encode('ascii', errors='replace').decode('ascii'))
