import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Move the h1 inside the login-box
pattern = r'<h1 style="color: var\(--primary\); font-size: 3rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">ClusterControl</h1>\s*<div class="login-box">'
replacement = """<div class="login-box">
            <h1 style="color: var(--primary); font-size: 2.2rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">ClusterControl</h1>"""

content = re.sub(pattern, replacement, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")

css_path = 'fastapi_app/static/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Update login-box css
css_pattern = r'\.login-box\s*\{[^\}]+\}'
new_css = """.login-box {
    width: 100%;
    max-width: 380px;
    padding: 40px 32px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4px);
}"""

css_content = re.sub(css_pattern, new_css, css_content)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("Updated style.css")

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove the collision block
js_collision_pattern = r'// Exclusion zone for the Title and Login Box.*?// Collision! Bounce out smoothly.*?\n\s*\}'
js_content = re.sub(js_collision_pattern, '', js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated main.js")

