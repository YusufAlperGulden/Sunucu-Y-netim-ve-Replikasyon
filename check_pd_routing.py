with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("} else if (hash === 'project-detail-view') {")
print(js[idx-100:idx+600].encode('ascii', errors='replace').decode('ascii'))
