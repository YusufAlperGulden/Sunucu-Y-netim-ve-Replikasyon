import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# find the switch to backups logic
if "renderBackups();" not in content.split("showView('backups-view')")[-1][:200]:
    content = content.replace("showView('backups-view');", "showView('backups-view');\n        renderBackups();")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added renderBackups() call")
else:
    print("Already calling renderBackups")
