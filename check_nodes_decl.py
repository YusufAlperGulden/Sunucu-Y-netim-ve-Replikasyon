with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('nodesPageData')
print(content[max(0, idx-500):idx+500])
