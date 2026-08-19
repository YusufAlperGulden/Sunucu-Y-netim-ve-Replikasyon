import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change the status card numbers
content = content.replace(
    '<div style="color: var(--success); font-size: 1.5rem; font-weight: 500;">34</div>',
    '<div style="color: var(--success); font-size: 1.5rem; font-weight: 500;">4</div>'
)
content = content.replace(
    '<div style="color: var(--primary); font-size: 1.5rem; font-weight: 500;">2</div>',
    '<div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">0</div>'
)
content = content.replace(
    '<div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">36</div>',
    '<div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">4</div>'
)

# Fix Edit Node Modal
# Change background: rgba(0,0,0,0.3); to background: #f9fafb; in modal-edit-node
content = content.replace('background: rgba(0,0,0,0.3);', 'background: #f9fafb;')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML patched")
