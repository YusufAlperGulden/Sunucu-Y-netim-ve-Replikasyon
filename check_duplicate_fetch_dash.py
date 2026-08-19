with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'function fetchDashboardMetrics', js)]
print("Number of definitions of fetchDashboardMetrics:", len(matches))
for m in matches:
    print("Definition at", m, ":", js[m:m+250].encode('ascii', errors='replace').decode('ascii'))
