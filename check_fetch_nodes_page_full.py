with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('window.fetchNodesPage = async function')
print(js[idx:idx+3500].encode('ascii', errors='replace').decode('ascii'))
