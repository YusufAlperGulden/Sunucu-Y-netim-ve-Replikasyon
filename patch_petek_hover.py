import re

css_path = 'fastapi_app/static/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = """
/* Honeycomb Node Petek Hover Effect */
.node-petek {
    transition: fill 0.2s, stroke 0.2s;
}
.node-hex-hover:hover .node-petek {
    fill: #ffffff !important;
    stroke: var(--success) !important;
}
"""
css_content += new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("Updated style.css")
