with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderNodesPage(')
if idx == -1:
    idx = content.find('renderNodesPage')
print(content[idx:idx+1500])
