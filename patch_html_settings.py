import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Settings Tab Bar
old_tabs = """<div class="settings-tab" onclick="switchSettingsTab('cloud')" id="tab-cloud" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">Cloud storage credentials</div>
                        <div class="settings-tab" onclick="switchSettingsTab('notifications')" id="tab-notifications" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">Notification services</div>
                        <div class="settings-tab" onclick="switchSettingsTab('certificates')" id="tab-certificates" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">Certificate management</div>
                        <div class="settings-tab" onclick="switchSettingsTab('license')" id="tab-license" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">License</div>
                        <div class="settings-tab" onclick="switchSettingsTab('addons')" id="tab-addons" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">Addons</div>
                        <div class="settings-tab" onclick="switchSettingsTab('diagnostics')" id="tab-diagnostics" style="padding: 16px 0; color: var(--text-main); cursor: pointer;">Diagnostics</div>"""

content = content.replace(old_tabs, "")

# Delete all those other panes
for pane in ['cloud', 'notifications', 'certificates', 'license', 'addons', 'diagnostics']:
    pattern = r'<div id="settings-content-' + pane + r'" class="settings-content-pane"[\s\S]*?</div>\s*</div>'
    # Wait, some panes might not have inner divs, let's just do it manually with regex carefully
    # Actually, they are inside <div id="settings-view">
    pass

# Let's just modify the profile content to have IDs
old_profile = """<div style="width: 90px; height: 90px; border-radius: 50%; background: #ffebeb; color: #e50000; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 400; margin-bottom: 20px;">SK</div>
                        <div style="font-size: 2rem; font-weight: 500; color: var(--text-main); margin-bottom: 4px;">Stajyer Kullanc</div>
                        <div style="font-size: 1rem; color: var(--text-muted); margin-bottom: 30px;">stajyer@tp.com</div>
                        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.95rem; margin-bottom: 40px; color: var(--text-secondary);">
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Time zone:</span><span style="width: 180px;">UTC</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Username:</span><span style="width: 180px; font-weight: 500;">stajyer@tp.com</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Team:</span><span style="width: 180px;">admins</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Origin:</span><span style="width: 180px;">cmon</span></div>
                        </div>"""

new_profile = """<div id="profile-avatar" style="width: 90px; height: 90px; border-radius: 50%; background: #e0e7ff; color: #4338ca; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 400; margin-bottom: 20px; text-transform: uppercase;">U</div>
                        <div id="profile-fullname" style="font-size: 2rem; font-weight: 500; color: var(--text-main); margin-bottom: 4px; text-transform: capitalize;">User</div>
                        <div id="profile-role" style="font-size: 1rem; color: var(--text-muted); margin-bottom: 30px; text-transform: uppercase;">ROLE</div>
                        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.95rem; margin-bottom: 40px; color: var(--text-secondary);">
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Time zone:</span><span style="width: 180px;">UTC</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Username:</span><span id="profile-username" style="width: 180px; font-weight: 500;">user</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Team:</span><span id="profile-team" style="width: 180px;">users</span></div>
                            <div style="display: flex; gap: 8px; justify-content: center;"><span style="color: var(--text-muted); width: 80px; text-align: right;">Origin:</span><span style="width: 180px;">Local DB</span></div>
                        </div>"""

if "profile-avatar" not in content:
    content = content.replace(old_tabs, "") # just in case
    # Replace profile content using regex to be safe about encoding chars
    content = re.sub(r'<div style="width: 90px; height: 90px;.*?</div>\s*</div>', new_profile, content, flags=re.DOTALL)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned up Settings tabs and updated Profile")
else:
    print("Already cleaned up")
