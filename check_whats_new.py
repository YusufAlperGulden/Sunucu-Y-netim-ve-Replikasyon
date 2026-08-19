with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="v1-4-2"')
idx_next = html.find('id="v1-4-1"')
print(html[idx:idx_next].encode('ascii', errors='replace').decode('ascii'))
