content = open('fastapi_app/static/main.js', encoding='utf-8').read()

hr_idx = content.find('function handleRouting()')
hr_chunk = content[hr_idx:hr_idx+1800]
print(hr_chunk)
