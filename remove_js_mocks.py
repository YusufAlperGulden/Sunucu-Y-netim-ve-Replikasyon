import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove dead disabledNode code
content = re.sub(r'// Determine if there is a disabled node\s+let disabledNode = null;\s+if \(proj\.nodes && proj\.nodes\.length > 0\) \{\s+// For demonstration[^\}]+disabledNode = proj\.nodes\[0\];\s+\}\s+\}', '', content)

# Remove mock report generation
content = re.sub(r'// Create a mock report in the table.*?tbody\.prepend\(tr\);\s+\}', '', content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed JS mocks.")
