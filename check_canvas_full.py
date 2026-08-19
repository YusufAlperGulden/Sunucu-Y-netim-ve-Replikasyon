with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

print(js[1000:2500].encode('ascii', errors='replace').decode('ascii'))
