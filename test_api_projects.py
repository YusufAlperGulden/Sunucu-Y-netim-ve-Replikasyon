import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects"
req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
req.add_header("Authorization", f"Basic {auth}")

resp = urllib.request.urlopen(req, context=ctx, timeout=15)
projects = json.loads(resp.read().decode('utf-8'))
print(f"Projects returned: {len(projects)}")
for p in projects:
    print(f" - Project ID={p['id']}, Name={p['name']}, Nodes={len(p.get('nodes', []))}")
    for n in p.get('nodes', []):
        print(f"    * Node ID={n['id']}, Name={n['name']}, Role={n['role']}")
