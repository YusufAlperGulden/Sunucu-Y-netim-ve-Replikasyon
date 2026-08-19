import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

auth_patch = """
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_credentials(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not access_token.startswith("token_"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    username = access_token.replace("token_", "", 1)
    from models import User
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
"""

# replace the old verify_credentials
import re
content = re.sub(r'def verify_credentials\(request: Request\):.*?raise HTTPException\(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"\)', auth_patch, content, flags=re.DOTALL)

login_patch = """
@app.post("/api/login")
def login(request: Request, db: Session = Depends(get_db)):
    from models import User
    data = asyncio.run(request.json())
    username = data.get("username")
    password = data.get("password")
    
    # Check if DB is empty, bootstrap from env if necessary
    admin_user = os.environ.get("ADMIN_USER", "admin")
    admin_pass = os.environ.get("ADMIN_PASS", "admin")
    if db.query(User).count() == 0:
        default_admin = User(username=admin_user, password_hash=get_password_hash(admin_pass), role="admin")
        db.add(default_admin)
        db.commit()
        
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return JSONResponse(status_code=401, content={"success": False, "message": "Invalid username or password"})
        
    response = JSONResponse(content={"success": True})
    response.set_cookie(key="access_token", value=f"token_{user.username}", httponly=True, max_age=86400, samesite="Lax")
    response.set_cookie(key="user_role", value=user.role, httponly=False, max_age=86400, samesite="Lax")
    return response
"""

# replace the old login
content = re.sub(r'@app\.post\("/api/login"\)\ndef login\(request: Request\):.*?return response', login_patch, content, flags=re.DOTALL)

user_routes = """
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

@app.get("/api/users", dependencies=[Depends(verify_credentials)])
def get_users(db: Session = Depends(get_db)):
    from models import User
    users = db.query(User).order_by(User.id.asc()).all()
    return [{"id": u.id, "username": u.username, "role": u.role, "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else ""} for u in users]

@app.post("/api/users", dependencies=[Depends(verify_credentials)])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    from models import User
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        return JSONResponse(status_code=400, content={"message": "Username already exists"})
    new_user = User(username=payload.username, password_hash=get_password_hash(payload.password), role=payload.role)
    db.add(new_user)
    db.commit()
    return {"success": True}

@app.delete("/api/users/{user_id}", dependencies=[Depends(verify_credentials)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    from models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    if db.query(User).count() == 1:
        return JSONResponse(status_code=400, content={"message": "Cannot delete the last user"})
    db.delete(user)
    db.commit()
    return {"success": True}
"""

if "@app.get(\"/api/users\"" not in content:
    content += "\n" + user_routes

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.py with User APIs")
