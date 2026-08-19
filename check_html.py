content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
import re
sections = re.findall(r'section id="([^"]+)"', content)
print('All section IDs:', sections)
nodes_links = [line.strip() for line in content.split('\n') if 'data-view' in line and 'nodes' in line.lower()]
print('Nodes links:', nodes_links[:5])
print('nodes-page-tbody count:', content.count('nodes-page-tbody'))
