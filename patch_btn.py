import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace <span>Clusters</span> with <span id="btn-back-projects" style="cursor: pointer; color: var(--primary);">Clusters</span>
content = content.replace('<span>Clusters</span> / <span id="detail-proj-breadcrumb-name"', '<span id="btn-back-projects" style="cursor: pointer; color: var(--primary);">Clusters</span> / <span id="detail-proj-breadcrumb-name"')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added btn-back-projects to index.html")
