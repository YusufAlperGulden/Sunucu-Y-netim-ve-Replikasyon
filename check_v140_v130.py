with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print("HTML matches:")
for m in re.finditer(r'v1[.-]4[.-]0|v1[.-]3[.-]0', html):
    print(html[max(0, m.start()-40):min(len(html), m.start()+80)])

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("\nJS matches:")
for m in re.finditer(r'v1[.-]4[.-]0|v1[.-]3[.-]0', js):
    print(js[max(0, m.start()-40):min(len(js), m.start()+80)])
