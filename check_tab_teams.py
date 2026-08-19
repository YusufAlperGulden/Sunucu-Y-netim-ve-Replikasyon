with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-teams"')
print(html[idx:idx+3500].encode('ascii', errors='replace').decode('ascii'))
