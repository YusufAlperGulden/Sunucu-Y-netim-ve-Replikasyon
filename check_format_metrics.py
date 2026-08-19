with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('m.status === \'online\'')
print(js[idx-100:idx+1500].encode('ascii', errors='replace').decode('ascii'))
