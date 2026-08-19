content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
idx = content.find('nodes-page-tbody')
# Look further back
chunk = content[max(0,idx-8000):idx]
import re
sections = list(re.finditer(r'<section[^>]*>', chunk))
print("Sections found in last 8000 chars before table:", len(sections))
for s in sections[-3:]:
    print(" ", s.group()[:100])

# find the "Nodes" heading or node-status-card
node_header_idx = chunk.rfind('node-status-card')
print("node-status-card position from start of chunk:", node_header_idx)
print("Surrounding context:", repr(chunk[max(0,node_header_idx-300):node_header_idx+50]))
