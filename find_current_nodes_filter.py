with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'currentNodesFilter', js)]
print("Matches:", len(matches))
for m in matches:
    print(f"Match at {m}:", js[m-50:m+250].encode('ascii', errors='replace').decode('ascii'))
