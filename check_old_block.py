with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

print(js[136700:143350].encode('ascii', errors='replace').decode('ascii'))
