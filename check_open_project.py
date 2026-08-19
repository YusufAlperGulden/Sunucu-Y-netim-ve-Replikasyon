with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = 13500
print(js[idx:idx+3500].encode('ascii', errors='replace').decode('ascii'))
