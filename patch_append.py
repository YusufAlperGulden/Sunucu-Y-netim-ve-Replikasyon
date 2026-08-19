import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "document.getElementById('cc-clusters-list').appendChild(clusterCard);",
    "if (document.getElementById('cc-clusters-list')) { document.getElementById('cc-clusters-list').appendChild(clusterCard); }"
)

content = content.replace(
    "tbody.appendChild(tr);",
    "if (tbody) { tbody.appendChild(tr); }"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added guards to appendChild")
