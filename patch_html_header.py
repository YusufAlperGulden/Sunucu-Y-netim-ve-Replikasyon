import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Demo ClusterControl", "<span id='header-username-display'>Demo ClusterControl</span>")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added header-username-display")
