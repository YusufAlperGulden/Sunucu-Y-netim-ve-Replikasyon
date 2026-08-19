with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="modal-backup-type-select"')
print(html[idx+2000:idx+5500].encode('ascii', errors='replace').decode('ascii'))
