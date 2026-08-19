with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('.modal-content')
print(html[idx-100:idx+600].encode('ascii', errors='replace').decode('ascii'))
