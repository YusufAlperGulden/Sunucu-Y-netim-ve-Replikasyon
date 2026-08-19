import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the center text
center_text_html = """<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                                  <div id="cc-donut-center-text" style="font-size: 1.5rem; font-weight: bold; color: var(--success);">0</div>
                                  <div style="font-size: 0.8rem; color: var(--text-muted);">Operational</div>
                              </div>"""

content = content.replace(center_text_html, "")

# Add the tooltip div at the end of the body
tooltip_html = """
<div id="donut-hover-tooltip" style="display: none; position: fixed; background: white; border: 1px solid #e5e7eb; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 6px 10px; font-size: 0.75rem; color: #6b7280; z-index: 10002; pointer-events: none; font-weight: 500;">
    <span id="donut-hover-text"></span>
</div>
"""

content = content.replace('</body>', tooltip_html + '\n  </body>')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML patched for donut tooltip")
