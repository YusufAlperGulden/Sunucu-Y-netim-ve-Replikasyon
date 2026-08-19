with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'nodesPageData' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
