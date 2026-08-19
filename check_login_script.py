with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('login-btn')
if idx == -1:
    idx = js.find('login-form')
if idx == -1:
    idx = js.find('login')

print(js[idx:idx+1500].encode('ascii', errors='replace').decode('ascii'))
