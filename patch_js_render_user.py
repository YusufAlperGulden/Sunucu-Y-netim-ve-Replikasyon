import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "fetchUsers();" not in content.split("showView('users-view')")[-1][:200]:
    content = content.replace("showView('users-view');", "showView('users-view');\n        fetchUsers();")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added fetchUsers() call")
else:
    print("Already calling fetchUsers")
