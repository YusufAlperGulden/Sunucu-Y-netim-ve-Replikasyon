with open('fastapi_app/vault.py', 'r', encoding='utf-8') as f:
    vault = f.read()

print("vault.py:")
print(vault[:1500].encode('ascii', errors='replace').decode('ascii'))
