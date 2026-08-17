import os
with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix verify_credentials
verify_bad = '''def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return credentials'''

verify_good = '''import os

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    admin_user = os.environ.get("ADMIN_USER")
    admin_pass = os.environ.get("ADMIN_PASS")
    if not admin_user or not admin_pass:
        raise ValueError("CRITICAL: ADMIN_USER or ADMIN_PASS environment variables are missing.")

    correct_username = secrets.compare_digest(credentials.username, admin_user)
    correct_password = secrets.compare_digest(credentials.password, admin_pass)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return credentials'''
text = text.replace(verify_bad, verify_good)

# Add /api/auth/verify
auth_endpoint = '''@app.get("/api/auth/verify", dependencies=[Depends(verify_credentials)])
def verify_auth():
    return {"status": "ok"}
'''
# I'll insert it right after def get_db(): ... finally: db.close()
text = text.replace(
    'class ProjectCreate(BaseModel):',
    auth_endpoint + '\nclass ProjectCreate(BaseModel):'
)

# Fix check_and_protect_wal_bloat signature
text = text.replace(
    'res = await check_and_protect_wal_bloat(primary.encrypted_url, proj.max_wal_lag_mb)',
    'res = await check_and_protect_wal_bloat(proj.id, primary.encrypted_url, proj.max_wal_lag_mb)'
)

# Fix setup_replication signature
text = text.replace(
    'result = await setup_replication(primary.encrypted_url, standby_urls)',
    'result = await setup_replication(project_id, primary.encrypted_url, standby_urls)'
)

with open('fastapi_app/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done modifying main.py')
