with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean_lines = lines[:89] + lines[95:]
with open('fastapi_app/main.py', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print("Cleaned up main.py lines 90-95")
