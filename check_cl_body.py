with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="v1-4-2"')
idx_end = html.find('<!-- Add Project Modal -->')
print(html[idx:idx_end].encode('ascii', errors='replace').decode('ascii'))
