content = open('fastapi_app/templates/index.html', encoding='utf-8').read()

NEW_NODES_VIEW = '''<div id="nodes-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <!-- Header -->
        <div style="display: flex; align-items: center; margin-bottom: 24px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px;"><rect x="2" y="4" width="20" height="6" rx="1"></rect><rect x="2" y="14" width="20" height="6" rx="1"></rect><line x1="6" y1="7" x2="6.01" y2="7"></line><line x1="10" y1="7" x2="18" y2="7"></line><line x1="6" y1="17" x2="6.01" y2="17"></line><line x1="10" y1="17" x2="18" y2="17"></line></svg>
            <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Nodes</h2>
        </div>

        <!-- Status Filter Cards -->
        <div style="display: flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 16px; background: white;">
            <div class="node-status-card" onclick="filterNodes('Operational', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); border-bottom: 2px solid var(--primary); background: #f9fafb; cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Operational</div>
                <div style="color: var(--success); font-size: 1.5rem; font-weight: 500;" id="stat-operational">-</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('Failed', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Failed</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-failed">0</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('Offline', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Offline</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-offline">0</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('Shut Down', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Shut Down</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-shutdown">0</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('Recovering', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Recovering</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-recovering">0</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('Unknown State', this)" style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Unknown State</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-unknown">0</div>
            </div>
            <div class="node-status-card" onclick="filterNodes('All', this)" style="flex: 1; padding: 16px 20px; cursor: pointer;">
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">All</div>
                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;" id="stat-all">-</div>
            </div>
        </div>

        <!-- Nodes Table -->
        <div style="background: white; border: 1px solid var(--border); border-radius: 8px; overflow: hidden;">
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border); background: #f9fafb;">
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('host')">
                                Hostname <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-host">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('port')">
                                Port <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-port">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap;">IP</th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('status')">
                                Status <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-status">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('type')">
                                Type <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-type">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('role')">
                                Role <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-role">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('cluster')">
                                Cluster <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-cluster">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap;">Version</th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; cursor: pointer;" onclick="sortNodes('seen')">
                                Last seen <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;" id="nodes-sort-arrows-seen">&#9650;&#9660;</span>
                            </th>
                            <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: #374151; white-space: nowrap; text-align: center;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="nodes-page-tbody">
                        <tr><td colspan="10" style="text-align:center; padding: 40px; color: #6b7280;">Yükleniyor...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>'''

tag_start = 55532
found_end = 69537

new_content = content[:tag_start] + NEW_NODES_VIEW + content[found_end:]

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced nodes-view section")
print(f"Old length: {found_end - tag_start}")
print(f"New length: {len(NEW_NODES_VIEW)}")
