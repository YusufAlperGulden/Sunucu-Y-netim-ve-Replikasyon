with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('renderReports')
print(js[idx-30:idx+400].encode('ascii', errors='replace').decode('ascii'))
