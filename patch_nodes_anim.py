import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Nodes donut slice
old_nodes_slice = '<circle id="nodes-donut-slice" cx="100" cy="100" r="70" fill="none" stroke="var(--success)" stroke-width="20" stroke-dasharray="439.8 439.8" stroke-dashoffset="0" style="transform: rotate(-90deg); transform-origin: 50% 50%;"></circle>'
new_nodes_slice = '<circle id="nodes-donut-slice" cx="100" cy="100" r="70" fill="none" stroke="var(--success)" stroke-width="20" stroke-dasharray="439.8 439.8" stroke-dashoffset="439.8" style="transition: stroke-dashoffset 1s ease-out; transform: rotate(-90deg); transform-origin: 50% 50%;"></circle>'

content = content.replace(old_nodes_slice, new_nodes_slice)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Nodes donut animation patched")
