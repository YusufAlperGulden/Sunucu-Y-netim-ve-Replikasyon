import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

me_endpoint = """
@app.get("/api/users/me", dependencies=[Depends(verify_credentials)])
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    from models import User
    username = credentials.username
    user = db.query(User).filter(User.username == username).first()
    role = user.role if user else ("admin" if username == os.environ.get("ADMIN_USER") else "viewer")
    return {
        "username": username,
        "role": role,
        "team": "admins" if role == "admin" else "viewers"
    }
"""

if "@app.get(\"/api/users/me\"" not in content:
    # Just append it
    content += "\n" + me_endpoint
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added /api/users/me")
else:
    print("Already exists")
