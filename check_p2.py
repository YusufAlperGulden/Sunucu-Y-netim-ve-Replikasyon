content = open('fastapi_app/main.py', encoding='utf-8').read()
# Find the GET /api/projects route handler
idx = content.find('"/api/projects"')
# Search for the function after this
func_start = content.find('async def ', idx)
if func_start == -1:
    func_start = content.find('def ', idx)
print("Route definition at:", idx)
print("Function at:", func_start)
print(content[idx:func_start+1500])
