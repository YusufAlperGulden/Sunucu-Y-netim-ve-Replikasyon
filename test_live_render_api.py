import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/1/metrics"
req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
req.add_header("Authorization", f"Basic {auth}")

try:
    resp = urllib.request.urlopen(req, context=ctx, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    print("LIVE RENDER METRICS API RESPONSE:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Error calling live API:", e)
