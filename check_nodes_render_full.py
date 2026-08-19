with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderNodesPage')
print(content[idx:idx+4000].encode('ascii', errors='replace').decode('ascii'))
