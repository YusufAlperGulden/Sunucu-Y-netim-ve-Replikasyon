import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the extra closing div
pattern = r'</div> <!-- End of projects-view -->'
content = re.sub(pattern, '<!-- Removed extra closing div -->', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed extra closing div")
