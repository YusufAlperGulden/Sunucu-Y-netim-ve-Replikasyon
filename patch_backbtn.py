import re
js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

js_content = js_content.replace(
    "btnBackProjects.addEventListener('click', showProjectsView);", 
    "btnBackProjects.addEventListener('click', () => { window.location.hash = 'projects-view'; });"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated btnBackProjects logic")
