with open('fastapi_app/templates/login.html', 'r', encoding='utf-8') as f:
    login_html = f.read()

print(login_html[:2500].encode('ascii', errors='replace').decode('ascii'))
