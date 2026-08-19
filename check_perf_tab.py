with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-content-performance"')
print(html[idx:idx+1500].encode('ascii', errors='replace').decode('ascii'))
