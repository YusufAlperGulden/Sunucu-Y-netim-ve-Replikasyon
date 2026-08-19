with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('setTimeout(handleRouting, 10);')
print(js[idx-100:idx+300].encode('ascii', errors='replace').decode('ascii'))
