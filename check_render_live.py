import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
    resp = urllib.request.urlopen(req, context=ctx, timeout=10)
    print("Render Status:", resp.status)
    content = resp.read().decode('utf-8')
    if 'v=52' in content:
        print("Render is running v=52 (v1.4.5)!")
    elif 'v=51' in content:
        print("Render is still running v=51 (deploying...)")
    elif 'v=50' in content:
        print("Render is still running v=50 (deploying...)")
    else:
        print("Current version tag in Render HTML:", [line for line in content.split('\n') if 'main.js' in line])
except Exception as e:
    print("Render request error:", e)
