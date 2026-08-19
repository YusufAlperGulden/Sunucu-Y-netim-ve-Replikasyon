with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print("JS loading matches:")
for m in re.finditer(r'(loading-state|Loading|Yukleniyor|Yükleniyor)', js, re.IGNORECASE):
    print(js[max(0, m.start()-30):min(len(js), m.start()+70)].encode('ascii', errors='replace').decode('ascii'))

print("\nHTML loading matches:")
for m in re.finditer(r'(loading-state|Loading|Yukleniyor|Yükleniyor)', html, re.IGNORECASE):
    print(html[max(0, m.start()-30):min(len(html), m.start()+70)].encode('ascii', errors='replace').decode('ascii'))
