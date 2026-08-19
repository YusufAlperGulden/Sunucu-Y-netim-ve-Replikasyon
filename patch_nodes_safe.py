import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

nodes_view_new = """            <!-- NODES VIEW -->
            <div id="nodes-view" class="view-section" style="display: none;">
                <div style="padding: 24px;">
                    <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; border: 1px solid var(--border); background: white;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><rect x="2" y="4" width="20" height="6" rx="1" ry="1"></rect><rect x="2" y="14" width="20" height="6" rx="1" ry="1"></rect><line x1="6" y1="7" x2="6.01" y2="7"></line><line x1="10" y1="7" x2="18" y2="7"></line><line x1="6" y1="17" x2="6.01" y2="17"></line><line x1="10" y1="17" x2="18" y2="17"></line></svg>
                        <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Nodes</h2>
                    </div>

                    <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); padding: 24px;">
                        
                        <!-- Status Cards -->
                        <div style="display: flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 16px;">
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); border-bottom: 2px solid var(--primary); background: #f9fafb; cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Operational</div>
                                <div style="color: var(--success); font-size: 1.5rem; font-weight: 500;">34</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Failed</div>
                                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">0</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Offline</div>
                                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">0</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Shut Down</div>
                                <div style="color: var(--primary); font-size: 1.5rem; font-weight: 500;">2</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Recovering</div>
                                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">0</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; border-right: 1px solid var(--border); cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Unknown State</div>
                                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">0</div>
                            </div>
                            <div style="flex: 1; padding: 16px 20px; cursor: pointer;">
                                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">All</div>
                                <div style="color: var(--text-main); font-size: 1.5rem; font-weight: 500;">36</div>
                            </div>
                        </div>

                        <!-- View Button -->
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                            <button style="display: flex; align-items: center; gap: 8px; background: white; border: 1px solid var(--border); border-radius: 6px; padding: 6px 12px; font-size: 0.85rem; font-weight: 500; color: var(--text-main); cursor: pointer;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                                View
                            </button>
                        </div>

                        <!-- Nodes Table -->
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                <thead>
                                    <tr style="border-bottom: 1px solid var(--glass-border); background: white;">
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Hostname <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Port <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">IP</th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Status <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Type <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Role <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Cluster <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Version</th>
                                        <th style="padding: 12px 16px; font-weight: 600; font-size: 0.8rem; color: var(--text-main); white-space: nowrap;">Last seen <span style="color: #a0aec0; margin-left:4px; font-size:0.6rem;">&#9650;&#9660;</span></th>
                                    </tr>
                                </thead>
                                <tbody id="nodes-page-tbody">
                                    <!-- Injected via JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>"""

start_idx = content.find('<!-- NODES VIEW -->')
end_idx = content.find('<!-- CLUSTERS VIEW -->', start_idx)

content = content[:start_idx] + nodes_view_new + "\n\n            " + content[end_idx:]

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Nodes view HTML safely patched")
