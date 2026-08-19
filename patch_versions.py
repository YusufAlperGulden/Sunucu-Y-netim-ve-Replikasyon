# -*- coding: utf-8 -*-
with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace version: '16.2' with version: '18.4'
content = content.replace("version: '16.2'", "version: '18.4'")

# Replace PostgreSQL Streaming v16 with PostgreSQL Streaming v18.4
content = content.replace("let vendor = 'PostgreSQL Streaming v16';", "let vendor = 'PostgreSQL Streaming v18.4';")

# Also, MariaDB version in nodesPageData is 11.4 but in tooltip it is 11.8. Let's make both 11.8 for consistency.
content = content.replace("version: '11.4'", "version: '11.8'")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Versions updated in main.js")
