with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'nodesPageData', content)]
for m in matches:
    print("nodesPageData at:", content[max(0, m-50):min(len(content), m+100)])
