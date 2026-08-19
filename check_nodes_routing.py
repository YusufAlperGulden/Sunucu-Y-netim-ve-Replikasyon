with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("} else if (hash === 'nodes-view') {")
print(js[idx-50:idx+300].encode('ascii', errors='replace').decode('ascii'))
