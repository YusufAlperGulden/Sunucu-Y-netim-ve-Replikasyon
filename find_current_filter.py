with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'currentFilter', js)]
for m in matches:
    print(js[max(0, m-50):min(len(js), m+150)].encode('ascii', errors='replace').decode('ascii'))
