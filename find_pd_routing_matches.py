with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'project-detail-view', js)]
for m in matches:
    print("Match at", m, ":", js[m-50:m+250].encode('ascii', errors='replace').decode('ascii'))
