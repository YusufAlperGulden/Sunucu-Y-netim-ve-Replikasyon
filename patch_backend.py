import re
from urllib.parse import urlparse
import sys

main_py_path = 'fastapi_app/main.py'
with open(main_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_get_detail = """    nodes = [{"id": n.id, "role": n.role, "name": n.name} for n in proj.nodes]
    return {"""

new_get_detail = """    from vault import decrypt
    from urllib.parse import urlparse
    nodes = []
    for n in proj.nodes:
        ip = "Unknown"
        port = "Unknown"
        db_type = "Unknown"
        try:
            if n.encrypted_url:
                url = decrypt(n.encrypted_url)
                parsed = urlparse(url)
                ip = parsed.hostname or "Unknown"
                port = str(parsed.port) if parsed.port else ("5432" if parsed.scheme == "postgresql" else "Unknown")
                db_type = "PostgreSQL" if parsed.scheme == "postgresql" else (parsed.scheme or "Unknown")
        except Exception:
            pass
        nodes.append({
            "id": n.id, 
            "role": n.role, 
            "name": n.name,
            "ip": ip,
            "port": port,
            "type": db_type,
            "status": "Operational",
            "version": "16.4" # Or fetch from DB if available
        })
    return {"""

if old_get_detail in content:
    content = content.replace(old_get_detail, new_get_detail)
else:
    print("Could not find old_get_detail")
    sys.exit(1)

with open(main_py_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated backend to return real node data")
