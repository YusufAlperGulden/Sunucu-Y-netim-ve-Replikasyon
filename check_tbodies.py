with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all tbody and initial loading elements
tbodies = re.findall(r'<tbody[^>]*>.*?</tbody>', content, re.DOTALL)
for tb in tbodies:
    print("--- TBODY ---")
    print(tb[:200].encode('ascii', errors='replace').decode('ascii'))
