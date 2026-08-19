import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will use a robust regex to find this block and delete it.
pattern = r'<div style="color: #4b5563; font-size: 0\.85rem; cursor: default; padding-left: 13px; opacity: 0\.7;">Cluster <br><span.*?</div>\s*</div>'

if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Deleted orphaned placeholder tags and fixed structure")
else:
    print("Could not find orphaned placeholder block")
