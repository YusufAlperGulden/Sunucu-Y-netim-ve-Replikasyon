with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-content-nodes"')
print(html[idx+2000:idx+4500].encode('ascii', errors='replace').decode('ascii'))
