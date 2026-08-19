with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="activity-view"')
idx_end = html.find('id="reports-view"')
print(html[idx:idx_end].encode('ascii', errors='replace').decode('ascii'))
