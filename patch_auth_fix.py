import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_auth = """def verify_credentials(request: Request, db: Session = Depends(get_db)):
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
    return user"""

good_auth = """from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
        
    from models import User
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # If no users exist in DB, fallback to ENV
    if db.query(User).count() == 0:
        correct_username = secrets.compare_digest(credentials.username, os.environ.get("ADMIN_USER", "admin"))
        correct_password = secrets.compare_digest(credentials.password, os.environ.get("ADMIN_PASS", "admin"))
        if correct_username and correct_password:
            return credentials
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials", headers={"WWW-Authenticate": "Bearer"})
    return credentials"""

if bad_auth in content:
    content = content.replace(bad_auth, good_auth)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed verify_credentials to use Basic Auth against DB")
else:
    print("bad_auth not found")
