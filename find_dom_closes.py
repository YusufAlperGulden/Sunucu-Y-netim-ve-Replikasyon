with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = 136709
idx2 = js.find("});", idx + 2000)
# search further down
while idx2 != -1 and idx2 < idx + 10000:
    print(f"Found }}); at {idx2}")
    print(js[idx2-50:idx2+50].encode('ascii', errors='replace').decode('ascii'))
    idx2 = js.find("});", idx2 + 1)
