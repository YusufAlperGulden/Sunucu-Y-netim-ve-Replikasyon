import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find handleRouting
idx = content.find('function handleRouting()')
print("handleRouting chunk:")
print(content[idx:idx+1500])

print("\n--- Let's search for DOMContentLoaded and initial route triggers ---")
matches = [m.start() for m in re.finditer(r'handleRouting', content)]
for m in matches:
    print("handleRouting reference at:", content[max(0, m-50):min(len(content), m+100)])
