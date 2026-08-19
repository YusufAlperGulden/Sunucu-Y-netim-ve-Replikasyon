import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

activity_view = re.search(r'(<section id="activity-view".*?</section>)', content, re.DOTALL).group(1)
opens = len(re.findall(r'<div', activity_view))
closes = len(re.findall(r'</div>', activity_view))
print(f"Activity view divs: opens={opens}, closes={closes}")
