content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
idx = content.find('id="activity-view"')
print(repr(content[idx:idx+3000]))
