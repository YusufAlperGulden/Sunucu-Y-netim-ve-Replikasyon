import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_settings_tab = """<div id="tab-content-settings" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Settings unavailable.</div></div>"""

new_settings_tab = """<div id="tab-content-settings" class="tab-content" style="display: none; padding: 20px;">
    <!-- Top inner tabs -->
    <div style="display: flex; gap: 20px; border-bottom: 1px solid var(--border); margin-bottom: 20px;">
        <div style="color: var(--primary); font-weight: 500; font-size: 0.9rem; padding-bottom: 10px; border-bottom: 2px solid var(--primary); cursor: pointer;">System settings</div>
        <div style="color: #6b7280; font-weight: 500; font-size: 0.9rem; padding-bottom: 10px; cursor: pointer;">Email notifications</div>
    </div>
    
    <!-- Search bar -->
    <div style="margin-bottom: 20px;">
        <input type="text" placeholder="Search by parameter, value, description" style="width: 100%; padding: 10px 15px; border: 1px solid var(--border); border-radius: 6px; background: white; outline: none; color: #374151; font-size: 0.9rem;">
    </div>
    
    <!-- Layout container -->
    <div style="display: flex; gap: 20px; min-height: 500px;">
        <!-- Left sidebar settings categories -->
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
        </div>
        
        <!-- Main content area -->
        <div style="flex: 1; background: white; border: 1px solid var(--border); border-radius: 8px; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead style="background: #f9fafb; border-bottom: 1px solid var(--border);">
                    <tr>
                        <th style="padding: 12px 20px; font-weight: 600; font-size: 0.8rem; color: #374151;">Parameter <span style="font-size: 0.6rem; color: #9ca3af;">▼</span></th>
                        <th style="padding: 12px 20px; font-weight: 600; font-size: 0.8rem; color: #374151;">Value <span style="font-size: 0.6rem; color: #9ca3af;">◆</span></th>
                        <th style="padding: 12px 20px; font-weight: 600; font-size: 0.8rem; color: #374151;">Description</th>
                    </tr>
                </thead>
                <tbody id="settings-tbody">
                    <!-- Javascript will populate this -->
                    <tr><td colspan="3" style="padding: 40px; text-align: center; color: #6b7280;">Loading settings...</td></tr>
                </tbody>
            </table>
            <!-- Pagination mock -->
            <div style="display: flex; justify-content: center; padding: 20px; gap: 10px; color: #6b7280; font-size: 0.85rem; align-items: center;">
                <span style="cursor: pointer;">&lt;</span>
                <span style="cursor: pointer; color: var(--primary); border: 1px solid var(--primary); border-radius: 4px; padding: 2px 8px;">1</span>
                <span style="cursor: pointer;">2</span>
                <span style="cursor: pointer;">3</span>
                <span style="cursor: pointer;">&gt;</span>
            </div>
        </div>
    </div>
</div>"""

if old_settings_tab in content:
    content = content.replace(old_settings_tab, new_settings_tab)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced settings tab HTML")
else:
    print("Could not find old_settings_tab")
