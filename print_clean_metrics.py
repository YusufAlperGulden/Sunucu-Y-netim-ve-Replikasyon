import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/2/metrics"
req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
req.add_header("Authorization", f"Basic {auth}")

resp = urllib.request.urlopen(req, context=ctx, timeout=15)
data = json.loads(resp.read().decode('utf-8'))

for n in data:
    m = n['metrics']
    print(f"=== {n['name']} ({n['role']}) ===")
    print(f"  Status:       {m['status']}")
    print(f"  Ping:         {m['ping']}")
    print(f"  Lag:          {m['lag']}")
    print(f"  Storage:      {m['storage']}")
    print(f"  Connections:  {m['connections']}")
    print(f"  Plates:       {m['plates']}")
    print(f"  Cache Hit:    {m['cache_hit']}")
    print(f"  Uptime:       {m['uptime']}")
    print(f"  Engine:       {m['version']}")
