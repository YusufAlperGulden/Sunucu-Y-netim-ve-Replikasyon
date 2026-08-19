with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('bubble-canvas')
if idx == -1:
    idx = js.find('canvas')
if idx != -1:
    print("Found in main.js at:", idx)
    print(js[idx-100:idx+1500].encode('ascii', errors='replace').decode('ascii'))
else:
    print("Not found in main.js")
