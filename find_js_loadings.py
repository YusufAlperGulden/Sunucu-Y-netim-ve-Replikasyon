with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Find all functions or blocks where innerHTML is set for loading
lines = js.split("\n")
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ["loading", "yukleniyor", "yükleniyor", "loading-state", "cc-loading"]):
        print(f"L{i+1}: {line.strip()[:120]}".encode('ascii', errors='replace').decode('ascii'))
