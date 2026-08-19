import urllib.request, ssl, time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for i in range(6):
    try:
        req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        content = resp.read().decode('utf-8')
        if 'v=52' in content:
            print(f"[{i*5}s] Render is NOW LIVE with v=52 (v1.4.5)!")
            break
        else:
            print(f"[{i*5}s] Still deploying v=51...")
    except Exception as e:
        print(f"[{i*5}s] Error:", e)
    time.sleep(5)
