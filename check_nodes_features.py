with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("filterNodes matches:")
for m in re.finditer(r'filterNodes', content):
    print(content[max(0, m.start()-50):min(len(content), m.start()+150)])

print("\nsortNodes matches:")
for m in re.finditer(r'sortNodes', content):
    print(content[max(0, m.start()-50):min(len(content), m.start()+150)])
