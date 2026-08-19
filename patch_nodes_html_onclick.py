import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add onclick handlers and classes to cards
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); border-bottom: 2px solid var(--primary); background: #f9fafb; cursor: pointer;">',
    '<div class="node-status-card" onclick="filterNodes(\'Operational\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); border-bottom: 2px solid var(--primary); background: #f9fafb; cursor: pointer;">'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Failed</div>',
    '<div class="node-status-card" onclick="filterNodes(\'Failed\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Failed</div>'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Offline</div>',
    '<div class="node-status-card" onclick="filterNodes(\'Offline\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Offline</div>'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Shut Down</div>',
    '<div class="node-status-card" onclick="filterNodes(\'Shut Down\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Shut Down</div>'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Recovering</div>',
    '<div class="node-status-card" onclick="filterNodes(\'Recovering\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Recovering</div>'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Unknown State</div>',
    '<div class="node-status-card" onclick="filterNodes(\'Unknown State\', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Unknown State</div>'
)
content = content.replace(
    '<div style="flex: 1; padding: 16px 20px; cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">All</div>',
    '<div class="node-status-card" onclick="filterNodes(\'All\', this)" style="flex: 1; padding: 16px 20px; cursor: pointer;">\n                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">All</div>'
)

# Add Actions column header
content = content.replace(
    '<th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Last seen <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>\n                                    </tr>',
    '<th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Last seen <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>\n                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap; text-align: center;">Actions</th>\n                                    </tr>'
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML patched")
