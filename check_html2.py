content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
# Find where the nodes-page-tbody lives - what section is it in?
idx = content.find('nodes-page-tbody')
snippet = content[max(0,idx-600):idx+100]
print(repr(snippet[-300:]))
