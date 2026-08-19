with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function showDetailView(proj)')
print(js[idx:idx+800].encode('ascii', errors='replace').decode('ascii'))
