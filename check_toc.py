content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
# Find and show the table of contents section
idx = content.find('Table of contents')
print(repr(content[idx:idx+1500]))
