with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('UI audit data collection</h2>')
print(html[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
