with open('fastapi_app/models.py', 'r', encoding='utf-8') as f:
    models_py = f.read()

idx = models_py.find('class Project')
print(models_py[idx:idx+1200].encode('ascii', errors='replace').decode('ascii'))
