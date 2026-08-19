with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's inspect where fetchActivityJobs and fetchActivityAlarms are defined
idx = js.find('window.switchActivityTab = function')
print(js[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
