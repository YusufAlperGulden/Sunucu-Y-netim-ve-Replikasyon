with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('renderNodesPage')
# Search backwards for document.addEventListener('DOMContentLoaded'
idx_dom = js.rfind("document.addEventListener('DOMContentLoaded'", 0, idx)
print("DOMContentLoaded at:", idx_dom)
print(js[idx_dom:idx+1500].encode('ascii', errors='replace').decode('ascii'))
