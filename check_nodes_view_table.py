with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="nodes-view"')
idx_end = html.find('id="backups-view"', idx)
print(html[idx:idx_end].encode('ascii', errors='replace').decode('ascii'))
