with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'fetchAuditLogs', js)]
for m in matches:
    print("MATCH at", m, ":", js[max(0, m-40):min(len(js), m+80)].encode('ascii', errors='replace').decode('ascii'))
