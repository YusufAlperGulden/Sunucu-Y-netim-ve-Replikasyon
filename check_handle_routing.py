with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function handleRouting')
if idx == -1:
    idx = js.find('handleRouting =')
if idx == -1:
    idx = js.find('handleRouting')

print(js[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
