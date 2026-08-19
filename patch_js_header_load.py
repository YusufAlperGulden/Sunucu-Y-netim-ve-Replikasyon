import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "setTimeout(fetchProfile, 10);" not in content:
    content = content.replace("setTimeout(handleRouting, 10);", "setTimeout(handleRouting, 10);\n    setTimeout(fetchProfile, 10);")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added fetchProfile on load")
