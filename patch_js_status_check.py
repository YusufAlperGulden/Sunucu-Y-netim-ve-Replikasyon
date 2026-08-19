import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where "m && m.ping !== undefined" starts and add better offline handling
old_check = "if(m && m.ping !== undefined) {"
new_check = "if(m && m.status === 'online') {"

if old_check in content:
    content = content.replace(old_check, new_check)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed online status check to use m.status")
else:
    print("Status check already updated or not found")
