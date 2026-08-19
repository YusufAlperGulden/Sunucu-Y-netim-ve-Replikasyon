import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the sidebar HTML block
old_sidebar = """        <!-- Left sidebar settings categories -->
        <div style="width: 200px; display: flex; flex-direction: column; gap: 15px;">
            <div style="color: var(--primary); font-size: 0.85rem; font-weight: 500; cursor: pointer; border-left: 3px solid var(--primary); padding-left: 10px;">Backup</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Cluster</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">CmonDB</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Controller</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Long Query</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Replication</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Retention</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Sampling</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Swapping</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">System</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Threshold</div>
        </div>"""

placeholder_span = '<br><span style="font-size: 0.65rem; color: #ef4444; font-weight: bold;">[PLACEHOLDER]</span>'

new_sidebar = f"""        <!-- Left sidebar settings categories -->
        <div style="width: 200px; display: flex; flex-direction: column; gap: 15px;">
            <div style="color: var(--primary); font-size: 0.85rem; font-weight: 500; cursor: pointer; border-left: 3px solid var(--primary); padding-left: 10px;">Backup</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Cluster {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">CmonDB {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Controller {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Long Query {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Replication {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Retention {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Sampling {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Swapping {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">System {placeholder_span}</div>
            <div style="color: #4b5563; font-size: 0.85rem; cursor: default; padding-left: 13px; opacity: 0.7;">Threshold {placeholder_span}</div>
        </div>"""

if old_sidebar in content:
    content = content.replace(old_sidebar, new_sidebar)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added placeholders to sidebar")
else:
    print("Could not find old_sidebar")

