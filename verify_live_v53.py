import urllib.request, ssl, time, json, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for i in range(10):
    try:
        req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        content = resp.read().decode('utf-8')
        if 'v=53' in content:
            print(f"[{i*4}s] Render is LIVE with v=53 (v1.4.6)!")
            
            # Test metrics API on live Render
            url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/2/metrics"
            m_req = urllib.request.Request(url)
            auth = base64.b64encode(b"admin:admin123").decode("ascii")
            m_req.add_header("Authorization", f"Basic {auth}")
            m_resp = urllib.request.urlopen(m_req, context=ctx, timeout=15)
            data = json.loads(m_resp.read().decode('utf-8'))
            print("Verified Live Project 2 Metrics from Render:")
            for n in data:
                print(f" - Node: {n['name']} ({n['role']}) -> Status: {n['metrics']['status']}, Ping: {n['metrics']['ping']}, Storage: {n['metrics']['storage']}, Xact: {n['metrics']['xact']}")
            break
        else:
            print(f"[{i*4}s] Deploying v=53...")
    except Exception as e:
        print(f"[{i*4}s] Wait error:", e)
    time.sleep(4)
