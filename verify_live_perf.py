import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/2/performance"
req = urllib.request.Request(url)
auth = base64.b64encode(b"admin:admin123").decode("ascii")
req.add_header("Authorization", f"Basic {auth}")

try:
    resp = urllib.request.urlopen(req, context=ctx, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    print("STATUS CODE: 200 OK")
    print("\n--- SAMPLE DB VARIABLES FROM LIVE POSTGRESQL (pg_settings) ---")
    for v in data.get('variables', [])[:6]:
        print(f" - {v['name']}: {v['setting']} {v['unit']} -> {v['desc']}")
        
    print("\n--- SCHEMA ANALYZER (Live Tables from Frankfurt Neon) ---")
    for s in data.get('schema', []):
        print(f" - Table: {s['table_name']:<20} | Columns: {s['col_count']:<2} | Rows: {s['row_count']}")
        
    print(f"\n--- DEADLOCKS DETECTED: {data.get('deadlocks')} ---")
except Exception as e:
    print("Error fetching from Render (might still be building):", e)
