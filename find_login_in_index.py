with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('Güvenli Giriş')
if idx == -1:
    idx = html.find('Giriş Yap')
if idx == -1:
    idx = html.find('login')

print("Found at:", idx)
if idx != -1:
    print(html[idx-500:idx+1500].encode('ascii', errors='replace').decode('ascii'))
