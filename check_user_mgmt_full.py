with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = 113600
print(html[idx:idx+4500].encode('ascii', errors='replace').decode('ascii'))
