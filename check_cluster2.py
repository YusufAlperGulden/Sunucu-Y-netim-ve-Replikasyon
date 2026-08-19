import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

cluster_view = re.search(r'(<div id="project-detail-view".*?)(<!-- DASHBOARD VIEW -->)', content, re.DOTALL).group(1)
opens = len(re.findall(r'<div', cluster_view))
closes = len(re.findall(r'</div>', cluster_view))
print(f"project-detail-view divs: opens={opens}, closes={closes}")
