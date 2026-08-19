for path in ['fastapi_app/static/main.js', 'fastapi_app/templates/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('v=42', 'v=43')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
print("Bumped to v=43")
