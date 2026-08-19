import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request("https://sunucu-yonetim-ve-replikasyon.onrender.com/")
    resp = urllib.request.urlopen(req, context=ctx, timeout=15)
    content = resp.read().decode('utf-8')
    print("Live Render HTML Status:")
    if 'v=61' in content:
        print(" -> Render is ALREADY updated to v=61 (v1.5.4)!")
    elif 'v=60' in content:
        print(" -> Render is currently running v=60 (deploy in progress...)")
    elif 'v=59' in content:
        print(" -> Render is currently running v=59 (deploy in progress...)")
    elif 'v=58' in content:
        print(" -> Render is currently running v=58 (deploy in progress...)")
    else:
        tags = [l for l in content.split('\n') if 'main.js' in l]
        print(" -> Live version tags:", tags)
        
    has_unavailable = 'Performance data unavailable' in content
    print(" -> Contains 'Performance data unavailable':", has_unavailable)
    has_perf_subtabs = 'perf-subtabs' in content
    print(" -> Contains 'perf-subtabs':", has_perf_subtabs)
except Exception as e:
    print("Error:", e)
