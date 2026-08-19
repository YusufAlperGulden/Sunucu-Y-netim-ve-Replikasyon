content = open('fastapi_app/main.py', encoding='utf-8').read()
import re
# Find all route definitions
routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"', content)
for method, path in routes:
    print(f"{method.upper():6} {path}")
