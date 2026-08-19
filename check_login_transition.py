with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('loginScreen.style.transition')
print(js[idx-600:idx+600].encode('ascii', errors='replace').decode('ascii'))
