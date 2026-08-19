import urllib.request, ssl, json, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Check HTML version tag
req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
resp = urllib.request.urlopen(req, context=ctx, timeout=10)
html = resp.read().decode('utf-8')
has_v53 = 'v=53' in html
has_v146 = 'v1.4.6' in html

print(f"Render HTTP Status: {resp.status}")
print(f"Contains asset version v=53: {has_v53}")
print(f"Contains release v1.4.6: {has_v146}")

# 2. Check live metrics endpoint
url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/2/metrics"
m_req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
m_req.add_header("Authorization", f"Basic {auth}")

m_resp = urllib.request.urlopen(m_req, context=ctx, timeout=15)
data = json.loads(m_resp.read().decode('utf-8'))
print(f"API /metrics Status: {m_resp.status}, Total Nodes Returned: {len(data)}")
for node in data:
    print(f" -> {node['name']} ({node['role']}): Status={node['metrics']['status']}, Ping={node['metrics']['ping']}")
