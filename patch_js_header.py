import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("if (team) team.innerText = data.team;", "if (team) team.innerText = data.team;\n            const headerUser = document.getElementById('header-username-display');\n            if (headerUser) headerUser.innerText = data.username;")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated fetchProfile with header")
