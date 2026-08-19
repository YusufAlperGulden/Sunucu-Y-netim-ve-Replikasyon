with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="modal-backup')
if idx == -1:
    idx = html.find('id="modal-create-backup')
if idx == -1:
    idx = html.find('Create a Backup')

print("Found modal at:", idx)
if idx != -1:
    print(html[idx-100:idx+2500].encode('ascii', errors='replace').decode('ascii'))
