import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("document.getElementById('stat-all').innerText = proj.nodes.length;", "if(document.getElementById('stat-all')) document.getElementById('stat-all').innerText = proj.nodes.length;")
content = content.replace("document.getElementById('stat-operational').innerText = proj.nodes.length; // Simplified for now", "if(document.getElementById('stat-operational')) document.getElementById('stat-operational').innerText = proj.nodes.length; // Simplified for now")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed TypeError stat-all")
