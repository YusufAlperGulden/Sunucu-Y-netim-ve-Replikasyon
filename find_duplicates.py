with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
for fn in ['renderNodesPage', 'filterNodes', 'sortNodes', 'fetchNodesPage']:
    matches = [m.start() for m in re.finditer(fn, js)]
    print(f"{fn} found {len(matches)} times at positions: {matches}")
