import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("table_name='database_nodes'", "table_name='nodes'")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed table name in debug endpoint")
