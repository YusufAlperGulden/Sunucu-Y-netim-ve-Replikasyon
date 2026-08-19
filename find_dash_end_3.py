with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx_start = 81190
print(js[idx_start+7000:idx_start+9000].encode('ascii', errors='replace').decode('ascii'))
