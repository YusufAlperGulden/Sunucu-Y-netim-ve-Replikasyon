with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's inspect fetchProjects and fetchRecentAlarms
idx = js.find('async function fetchProjects()')
print("fetchProjects:")
print(js[idx:idx+800].encode('ascii', errors='replace').decode('ascii'))

idx = js.find('async function fetchRecentAlarms()')
print("\nfetchRecentAlarms:")
print(js[idx:idx+800].encode('ascii', errors='replace').decode('ascii'))
