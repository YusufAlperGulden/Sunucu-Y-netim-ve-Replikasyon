models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("default=datetime.utcnow", "default=datetime.datetime.utcnow")

with open(models_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed datetime bug")
