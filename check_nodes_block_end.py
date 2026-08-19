with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("document.addEventListener('DOMContentLoaded'", 136709)
idx2 = js.find("});", idx+1000)
print(js[idx:idx2+500].encode('ascii', errors='replace').decode('ascii'))
