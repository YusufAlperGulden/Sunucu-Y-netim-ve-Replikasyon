import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace any ? or -? before Operational / Shut Down / etc
content = re.sub(r'[^\x00-\x7F]*\?\s*([0-9]*\s*Operational)', r'&#8226; \1', content)
content = re.sub(r'[^\x00-\x7F]*\?\s*([0-9]*\s*Shut Down)', r'&#8226; \1', content)
content = re.sub(r'[^\x00-\x7F]*\?\s*([0-9]*\s*Warning)', r'&#8226; \1', content)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML bullets fixed")
