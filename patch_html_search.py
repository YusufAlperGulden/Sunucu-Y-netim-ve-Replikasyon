import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_input = '<input type="text" placeholder="Search by parameter, value, description" style="width: 100%; padding: 10px 15px; border: 1px solid var(--border); border-radius: 6px; background: white; outline: none; color: #374151; font-size: 0.9rem;">'
new_input = '<input type="text" id="settings-search-input" placeholder="Search by parameter, value, description" style="width: 100%; padding: 10px 15px; border: 1px solid var(--border); border-radius: 6px; background: white; outline: none; color: #374151; font-size: 0.9rem;">'

if old_input in content:
    content = content.replace(old_input, new_input)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added id to search input")
else:
    # Try regex
    content = re.sub(r'<input type="text" placeholder="Search by parameter, value, description"[^>]*>', new_input, content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added id to search input with regex")
