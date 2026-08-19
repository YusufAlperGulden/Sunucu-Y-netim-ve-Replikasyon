models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text, Index", "from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text, Index, Float")

with open(models_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added Float to imports")
