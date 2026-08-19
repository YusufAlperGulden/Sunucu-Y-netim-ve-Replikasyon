import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace MariaDB with PostgreSQL for email nodes
content = content.replace("type: 'MariaDB'", "type: 'PostgreSQL'")
content = content.replace("port: '3306'", "port: '5432'")
content = content.replace("version: '11.8'", "version: '16.4'")

# Bump version to v=12
content = content.replace('v=11', 'v=12')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=11', 'v=12')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fixed MariaDB to PostgreSQL")
