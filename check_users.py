import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

users_view = re.search(r'(<section id="users-view".*?</section>)', content, re.DOTALL).group(1)
opens = len(re.findall(r'<div', users_view))
closes = len(re.findall(r'</div>', users_view))
print(f"Users view divs: opens={opens}, closes={closes}")
