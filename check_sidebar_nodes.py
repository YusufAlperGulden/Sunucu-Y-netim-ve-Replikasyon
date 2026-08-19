with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('data-view="nodes-view"')
print(html[idx-100:idx+200].encode('ascii', errors='replace').decode('ascii'))
