with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'Performance data unavailable|tab-content-performance', html)]
print("Matches in local index.html:", len(matches))
for m in matches:
    print(f"Match at {m}:", html[m-50:m+200].encode('ascii', errors='replace').decode('ascii'))
