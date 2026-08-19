import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
resp = urllib.request.urlopen(req, context=ctx, timeout=15)
content = resp.read().decode('utf-8')
print("Current Live Render Version:", [l.strip() for l in content.split('\n') if 'main.js' in l or 'v1.5.4' in l or 'v1.5.3' in l][:5])
