import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

backups_view = re.search(r'(<section id="backups-view".*?</section>)', content, re.DOTALL).group(1)
opens = len(re.findall(r'<div', backups_view))
closes = len(re.findall(r'</div>', backups_view))
print(f"Backups view divs: opens={opens}, closes={closes}")
