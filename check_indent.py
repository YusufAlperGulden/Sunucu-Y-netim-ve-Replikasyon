with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[50:110], 51):
    print(f"{i}: {repr(l)}")
