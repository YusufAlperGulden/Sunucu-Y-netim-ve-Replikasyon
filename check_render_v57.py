import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
    resp = urllib.request.urlopen(req, context=ctx, timeout=10)
    content = resp.read().decode('utf-8')
    if 'v=57' in content:
        print("Render is running v=57 (v1.5.0)!")
    elif 'v=56' in content:
        print("Render is running v=56 (deploying v57...)")
    elif 'v=55' in content:
        print("Render is running v=55 (deploying v57...)")
    else:
        print("Render HTML main.js version tag:", [l for l in content.split('\n') if 'main.js' in l])
except Exception as e:
    print("Error:", e)
