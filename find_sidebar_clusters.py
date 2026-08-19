with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'sidebar-clusters-list|sidebarClustersList|updateSidebarClusters', js)]
for m in matches:
    print("Match at", m, ":", js[m:m+300].encode('ascii', errors='replace').decode('ascii'))
