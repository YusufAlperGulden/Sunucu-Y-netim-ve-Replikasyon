import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("document.querySelector('#table-reports > div').style.display = 'block';", "document.getElementById('empty-reports-state').style.display = 'block';")
content = content.replace("document.querySelector('#table-reports table').style.display = 'none';", "document.getElementById('reports-table-element').style.display = 'none';")

content = content.replace("document.querySelector('#table-reports > div').style.display = 'none';", "document.getElementById('empty-reports-state').style.display = 'none';")
content = content.replace("document.querySelector('#table-reports table').style.display = 'table';", "document.getElementById('reports-table-element').style.display = 'table';")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated JS IDs")
