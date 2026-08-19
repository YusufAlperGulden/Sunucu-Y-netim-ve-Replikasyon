# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

center_text_html = """
                                      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;">
                                          <div id="nodes-donut-center-num" style="font-size: 1.5rem; font-weight: bold; color: var(--success);">0</div>
                                          <div style="font-size: 0.8rem; color: var(--text-muted);">Nodes</div>
                                      </div>
"""

# Insert it immediately after </svg> of nodes-donut-svg
content = re.sub(r'(<svg id="nodes-donut-svg".*?</svg>)', r'\1' + center_text_html, content, flags=re.DOTALL)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Nodes donut center text added via regex")
