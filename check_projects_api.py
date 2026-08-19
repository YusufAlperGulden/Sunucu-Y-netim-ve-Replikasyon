content = open('fastapi_app/main.py', encoding='utf-8').read()
# Find the /api/projects GET endpoint
idx = content.find('@app.get("/api/projects")')
print(content[idx:idx+1500])
