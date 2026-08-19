# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

nodes_donut_html = """                                  <div style="flex: 1; display: flex; align-items: center; justify-content: center; position: relative;">
                                      <svg id="nodes-donut-svg" width="180" height="180" viewBox="0 0 200 200" style="cursor: pointer;" onclick="document.querySelector('a[data-view=\\'nodes-view\\']').click()">
                                          <circle cx="100" cy="100" r="70" fill="none" stroke="#e5e7eb" stroke-width="20"></circle>
                                          <circle id="nodes-donut-slice" cx="100" cy="100" r="70" fill="none" stroke="var(--success)" stroke-width="20" stroke-dasharray="439.8 439.8" stroke-dashoffset="0" style="transform: rotate(-90deg); transform-origin: 50% 50%;"></circle>
                                      </svg>
                                      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;">
                                          <div id="nodes-donut-center-num" style="font-size: 1.5rem; font-weight: bold; color: var(--success);">0</div>
                                          <div style="font-size: 0.8rem; color: var(--text-muted);">Nodes</div>
                                      </div>
                                  </div>"""

# Find the nodes donut section
start_idx = content.find('<div style="flex: 1; display: flex; align-items: center; justify-content: center; position: relative;">\n                                      <svg id="nodes-donut-svg"')
if start_idx != -1:
    end_idx = content.find('</div>', content.find('</svg>', start_idx)) + 6
    content = content[:start_idx] + nodes_donut_html + content[end_idx:]

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML nodes donut patched")
