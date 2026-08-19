import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Fix sidebar navigation query selector
old_code = "const sidebarLinks = document.querySelectorAll('.sidebar-nav a');"
new_code = "const sidebarLinks = document.querySelectorAll('.sidebar-nav > a, .sidebar-nav > div > a, a[data-view=\"changelog-view\"]');"

js_content = js_content.replace(old_code, new_code)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated main.js")
