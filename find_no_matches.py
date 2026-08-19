with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'There are no matches', js)]
for m in matches:
    print("Match at:", m)
    print(js[max(0, m-200):min(len(js), m+300)].encode('ascii', errors='replace').decode('ascii'))
