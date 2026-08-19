import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

create_all_snippet = """from models import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI()"""

if "Base.metadata.create_all(bind=engine)" not in content:
    content = content.replace("app = FastAPI()", create_all_snippet)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added create_all")
else:
    print("create_all already exists")
