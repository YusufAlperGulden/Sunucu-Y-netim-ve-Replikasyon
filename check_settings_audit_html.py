with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'UI audit data collection|audit-data|download audit data', html, re.IGNORECASE)]
print("Matches in index.html:", len(matches))
for m in matches:
    print(f"Match at {m}:", html[m-50:m+250].encode('ascii', errors='replace').decode('ascii'))
