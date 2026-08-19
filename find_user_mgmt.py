with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'User management|Users|Teams|LDAP', html)]
for m in matches[:10]:
    print(f"Match at {m}:", html[m:m+150].encode('ascii', errors='replace').decode('ascii'))
