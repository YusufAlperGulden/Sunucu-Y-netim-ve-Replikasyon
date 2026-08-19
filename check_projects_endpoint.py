content = open('fastapi_app/main.py', encoding='utf-8').read()
# Find the GET /api/projects endpoint function
import re
m = re.search(r'@app\.get\("/api/projects"\).*?(?=@app\.|$)', content, re.DOTALL)
if m:
    print(m.group()[:2000])
