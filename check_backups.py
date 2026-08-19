with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('async function fetchBackups')
if idx != -1:
    print(js[idx:idx+600].encode('ascii', errors='replace').decode('ascii'))
