import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
resp = urllib.request.urlopen(req, context=ctx, timeout=15)
content = resp.read().decode('utf-8')
print("Render Live Status:")
if 'v=69' in content:
    print(" -> Render is UP TO DATE with v=69 (v1.6.2)!")
else:
    print(" -> Current version in Render HTML:", [l.strip() for l in content.split('\n') if 'main.js' in l][:3])

has_toggle_func = 'window.toggleUiAudit' in content or 'btn-toggle-ui-audit' in content
print(" -> Contains 'btn-toggle-ui-audit':", has_toggle_func)
