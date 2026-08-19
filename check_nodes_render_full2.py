with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderNodesPage')
print(content[idx+1800:idx+3500].encode('ascii', errors='replace').decode('ascii'))
