import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

index_activity = content.find('<section id="activity-view"')
before_activity = content[:index_activity]

opens = len(re.findall(r'<div\b', before_activity))
closes = len(re.findall(r'</div>', before_activity))
print(f"Before activity-view: opens={opens}, closes={closes}")

index_cluster = content.find('<div id="cluster-detail-view"')
before_cluster = content[:index_cluster]
print(f"Before cluster-detail-view: opens={len(re.findall(r'<div\b', before_cluster))}, closes={len(re.findall(r'</div>', before_cluster))}")

index_projects = content.find('<div id="projects-view"')
before_projects = content[:index_projects]
print(f"Before projects-view: opens={len(re.findall(r'<div\b', before_projects))}, closes={len(re.findall(r'</div>', before_projects))}")

