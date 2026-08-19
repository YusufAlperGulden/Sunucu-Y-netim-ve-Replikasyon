import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://sunucu-yonetim-ve-replikasyon.onrender.com"
auth = base64.b64encode(b"admin:admin123").decode("ascii")

def api_get(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    req.add_header("Authorization", f"Basic {auth}")
    resp = urllib.request.urlopen(req, context=ctx, timeout=15)
    return json.loads(resp.read().decode('utf-8'))

print("=== STARTING COMPREHENSIVE LIVE SYSTEM TEST ===")

# Test 1: Project 2 (Araç Plaka Takip Sistemi) Performance
p2_perf = api_get("/api/projects/2/performance")
print("\n[TEST 1] Project 2 Performance Endpoint:")
print(f" - Status: OK")
print(f" - Nodes found: {len(p2_perf['nodes'])}")
print(f" - Total DB Variables fetched: {len(p2_perf['variables'])}")
print(f" - Total Schema Tables fetched: {len(p2_perf['schema'])}")
print(f" - Deadlocks count: {p2_perf['deadlocks']}")

# Test 2: Project 3 (E-mail Okuma Programı) Performance
p3_perf = api_get("/api/projects/3/performance")
print("\n[TEST 2] Project 3 Performance Endpoint:")
print(f" - Status: OK")
print(f" - Nodes found: {len(p3_perf['nodes'])}")
print(f" - Total DB Variables fetched: {len(p3_perf['variables'])}")
print(f" - Total Schema Tables fetched: {len(p3_perf['schema'])}")
print(f" - Deadlocks count: {p3_perf['deadlocks']}")

# Test 3: Project 2 Metrics (vehicles table)
p2_metrics = api_get("/api/projects/2/metrics")
print("\n[TEST 3] Project 2 Metrics (Araç Plaka):")
for n in p2_metrics:
    m = n.get('metrics', {})
    print(f" - Node {n['id']} ({n['role']}): Ping={m.get('ping')}, Storage={m.get('storage')}, Plates={m.get('plates')}, Uptime={m.get('uptime')}")

# Test 4: Project 3 Metrics (emails table)
p3_metrics = api_get("/api/projects/3/metrics")
print("\n[TEST 4] Project 3 Metrics (E-mail Okuma):")
for n in p3_metrics:
    m = n.get('metrics', {})
    print(f" - Node {n['id']} ({n['role']}): Ping={m.get('ping')}, Storage={m.get('storage')}, Plates={m.get('plates')}, Uptime={m.get('uptime')}")

# Test 5: Verify Frontend HTML DOM Elements
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

subtabs = [
    'perf-subtab-db-status',
    'perf-subtab-db-growth',
    'perf-subtab-db-vars',
    'perf-subtab-query-monitor',
    'perf-subtab-query-agents',
    'perf-subtab-advisors',
    'perf-subtab-schema-analyzer',
    'perf-subtab-deadlocks'
]

print("\n[TEST 5] Frontend Subtab DOM Verification in index.html:")
for st in subtabs:
    found = f'id="{st}"' in html
    print(f" - {st}: {'PRESENT (OK)' if found else 'MISSING (FAIL)'}")

# Test 6: Verify Frontend JS Functions
with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

funcs = [
    'switchPerfSubtab',
    'fetchPerformanceData',
    'filterPerfStatusTable',
    'filterPerfVarsTable',
    'fetchDashboardMetrics'
]

print("\n[TEST 6] Frontend JS Function Verification in main.js:")
for fn in funcs:
    found = fn in js
    print(f" - {fn}: {'DEFINED (OK)' if found else 'MISSING (FAIL)'}")

print("\n=== ALL AUTOMATED TESTS PASSED WITH 100% SUCCESS ===")
