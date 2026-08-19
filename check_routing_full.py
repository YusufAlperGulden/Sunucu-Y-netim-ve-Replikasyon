with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function handleRouting()')
idx2 = content.find('window.addEventListener(\'hashchange\', handleRouting);')
print(content[idx:idx2+100])
