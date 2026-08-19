with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'function\s+fetchAuditLogs', js)]
for m in matches:
    print(js[m-20:m+500].encode('ascii', errors='replace').decode('ascii'))
