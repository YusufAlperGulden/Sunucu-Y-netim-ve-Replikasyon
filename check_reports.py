import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

reports_view = re.search(r'(<section id="reports-view".*?</section>)', content, re.DOTALL).group(1)
opens = len(re.findall(r'<div', reports_view))
closes = len(re.findall(r'</div>', reports_view))
print(f"Reports view divs: opens={opens}, closes={closes}")
