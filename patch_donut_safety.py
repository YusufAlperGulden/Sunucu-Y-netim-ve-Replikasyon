import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "document.getElementById('cc-donut-progress').style.strokeDashoffset = dashOffset1;",
    "const cdp = document.getElementById('cc-donut-progress'); if(cdp) cdp.style.strokeDashoffset = dashOffset1;"
)
content = content.replace(
    "document.getElementById('nodes-donut-progress').style.strokeDashoffset = dashOffset2;",
    "const ndp = document.getElementById('nodes-donut-progress'); if(ndp) ndp.style.strokeDashoffset = dashOffset2;"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched donut progress safety")
