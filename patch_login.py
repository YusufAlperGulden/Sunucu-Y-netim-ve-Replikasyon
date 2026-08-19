import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_login = """@app.post("/api/login")
def login(request: Request, db: Session = Depends(get_db)):
    from models import User
    data = asyncio.run(request.json())
    username = data.get("username")
    password = data.get("password")"""

good_login = """class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    from models import User
    username = payload.username
    password = payload.password"""

if bad_login in content:
    content = content.replace(bad_login, good_login)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed login endpoint")
else:
    print("bad_login not found")
