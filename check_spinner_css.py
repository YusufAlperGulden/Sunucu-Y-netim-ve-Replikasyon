with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect the style section where cc-spinner is or can be added/improved
idx = content.find('/* ---- LOADING SPINNER ---- */')
if idx != -1:
    print(content[idx:idx+800])
else:
    print("Spinner not found in index.html")
