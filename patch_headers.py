import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def make_th(label, col_id, has_sort=True):
    if not has_sort:
        return f'<th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">{label}</th>'
    
    return f'''<th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap; position: relative; cursor: pointer; user-select: none;" onmouseenter="document.getElementById('nodes-sort-tooltip-{col_id}').style.display='block'" onmouseleave="document.getElementById('nodes-sort-tooltip-{col_id}').style.display='none'" onclick="sortNodes('{col_id}')">
    {label} <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-{col_id}">&#9650;&#9660;</span>
    <div id="nodes-sort-tooltip-{col_id}" style="display: none; position: absolute; background: #111827; color: white; padding: 6px 10px; border-radius: 6px; font-size: 0.75rem; white-space: nowrap; top: -25px; left: 16px; z-index: 100; font-weight: 400;">
        <span id="nodes-sort-text-{col_id}">Click to sort ascending</span>
        <div style="position: absolute; bottom: -4px; left: 16px; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 4px solid #111827;"></div>
    </div>
</th>'''

headers = f"""<tr style="border-bottom: 1px solid var(--glass-border); background: white;">
    {make_th('Hostname', 'host')}
    {make_th('Port', 'port')}
    {make_th('IP', 'ip', has_sort=False)}
    {make_th('Status', 'status')}
    {make_th('Type', 'type')}
    {make_th('Role', 'role')}
    {make_th('Cluster', 'cluster')}
    {make_th('Version', 'version', has_sort=False)}
    {make_th('Last seen', 'seen')}
    <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap; text-align: center;">Actions</th>
</tr>"""

start_idx = content.find('<tr style="border-bottom: 1px solid var(--glass-border); background: white;">')
end_idx = content.find('</thead>', start_idx)

content = content[:start_idx] + headers + "\n                                " + content[end_idx:]

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML headers patched")
