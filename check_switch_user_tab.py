with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function switchUserTab')
if idx == -1:
    idx = js.find('switchUserTab')
print(js[idx-50:idx+800].encode('ascii', errors='replace').decode('ascii'))
