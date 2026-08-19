with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('sidebarLinks.forEach')
print(js[idx:idx+800].encode('ascii', errors='replace').decode('ascii'))
