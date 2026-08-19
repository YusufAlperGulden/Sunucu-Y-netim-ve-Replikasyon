import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_auth_1 = 'raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")'
new_auth_1 = 'raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})'

old_auth_2 = 'raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")'
new_auth_2 = 'raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials", headers={"WWW-Authenticate": "Bearer"})'

content = content.replace(old_auth_1, new_auth_1)
content = content.replace(old_auth_2, new_auth_2)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTTPException to use Bearer to bypass native popup")

