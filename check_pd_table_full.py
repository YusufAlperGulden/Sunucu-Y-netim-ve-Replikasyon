with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-content-nodes"')
print(html[idx+1200:idx+3500].encode('ascii', errors='replace').decode('ascii'))
