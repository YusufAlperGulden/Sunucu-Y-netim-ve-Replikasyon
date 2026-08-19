import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/3/metrics"
req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
req.add_header("Authorization", f"Basic {auth}")

resp = urllib.request.urlopen(req, context=ctx, timeout=15)
data = json.loads(resp.read().decode('utf-8'))
print("PROJECT 3 NODES FROM RENDER:")
print(json.dumps(data, indent=2))
