with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderNodesPage')
print("renderNodesPage block:")
print(content[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
