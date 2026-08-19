import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_back = """btnBackProjects.addEventListener('click', () => { window.location.hash = 'projects-view'; });"""
new_back = """btnBackProjects.addEventListener('click', () => { window.location.hash = 'clusters-view'; });"""

if old_back in content:
    content = content.replace(old_back, new_back)
else:
    print("Could not find back button listener")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated back button listener")
