import re

ha_path = 'fastapi_app/ha_manager.py'
with open(ha_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the xact format (currently has encoding issues)
content = re.sub(
    r"'xact': f'\{commits\}.*?/ \{rollbacks\}.*?',",
    "'xact': f'{commits} / {rollbacks}',",
    content
)

# Also make sure 'row_count' is exposed in addition to 'plates' 
content = content.replace(
    "'plates': plates_count,",
    "'plates': plates_count,\n                  'row_count': plates_count,"
)

# Fix the storage to display MB for large sizes
old_storage = "'storage': f'{int(db_size_kb)} kB',"
new_storage = """'storage': f'{db_size_kb/1024:.1f} MB' if db_size_kb > 1024 else f'{int(db_size_kb)} kB',"""

if old_storage in content:
    content = content.replace(old_storage, new_storage)

with open(ha_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed ha_manager.py return values")
