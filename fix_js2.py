import re
with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('${node.name}', '${escapeHTML(node.name)}')
text = text.replace('${node.role}', '${escapeHTML(node.role)}')
# Don't double escape if we ran it multiple times
text = text.replace('${escapeHTML(escapeHTML(node.name))}', '${escapeHTML(node.name)}')
text = text.replace('${escapeHTML(escapeHTML(node.role))}', '${escapeHTML(node.role)}')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
