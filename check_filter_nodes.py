with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('window.filterNodes = function')
print(content[idx-100:idx+1500])
