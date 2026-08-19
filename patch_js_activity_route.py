import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "hash === 'activity-view'" not in content:
    content = content.replace("else if (hash === 'audit-logs-view')", "else if (hash === 'activity-view' || hash === 'audit-logs-view')")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added activity-view to routing")
else:
    print("activity-view already in routing")
