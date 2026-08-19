import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Fix the syntax error in update()
pattern = r'update\(\) \{\s*this\.x \+= this\.vx;\s*this\.y \+= this\.vy;\s*else \{.*?\n\s*\}\s*\}'
replacement = """update() {
                this.x += this.vx;
                this.y += this.vy;
"""

js_content = re.sub(pattern, replacement, js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
