import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Activity Center view
activity_pattern = re.compile(r'<section id="activity-view" class="view-section" style="display: none;">(.*?)</section>', re.DOTALL)
new_activity = """<section id="activity-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; border: 1px solid var(--border); background: white;">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><path d="M19 3H5C3.9 3 3 3.9 3 5v14c0 1.1.9 2 2 2h7"></path><path d="M3 16l4-4 4 4"></path><path d="M8 11l3-3 3 3"></path><path d="M22 17c0 0-1.5-2.5-4-2.5S14 17 14 17s1.5 2.5 4 2.5S22 17 22 17z"></path><circle cx="18" cy="17" r="1"></circle></svg>
            <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Activity center</h2>
        </div>
        
        <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; padding: 40px; text-align: center;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
            <div style="color: #6b7280; font-size: 14px;">No activities or alarms recorded yet.</div>
        </div>
    </div>
</section>"""
content = activity_pattern.sub(new_activity, content)

# Replace Reports view
reports_pattern = re.compile(r'<section id="reports-view" class="view-section" style="display: none;">(.*?)</section>', re.DOTALL)
new_reports = """<section id="reports-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; border: 1px solid var(--border); background: white;">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="8" y1="8" x2="16" y2="8"></line><line x1="8" y1="12" x2="16" y2="12"></line><line x1="8" y1="16" x2="12" y2="16"></line></svg>
            <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Operational reports</h2>
        </div>
        
        <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; padding: 40px; text-align: center;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
            <div style="color: #6b7280; font-size: 14px;">No reports generated yet.</div>
        </div>
    </div>
</section>"""
content = reports_pattern.sub(new_reports, content)

# Replace Users view
users_pattern = re.compile(r'<section id="users-view" class="view-section" style="display: none;">(.*?)</section>', re.DOTALL)
new_users = """<section id="users-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); background: white;">
            <div style="display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><path d="M11.5 15H7a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M21.378 10.626a1 1 0 1 0-3.004-3.004l-4.01 4.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"></path></svg>
                <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">User management</h2>
            </div>
            <button class="btn-primary" style="display: flex; align-items: center; gap: 8px;">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                Create user or team
            </button>
        </div>
        
        <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; padding: 40px; text-align: center;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            <div style="color: #6b7280; font-size: 14px;">No other users created yet.</div>
        </div>
    </div>
</section>"""
content = users_pattern.sub(new_users, content)

# Replace Backups view
backups_pattern = re.compile(r'<section id="backups-view" class="view-section" style="display: none;">(.*?)</section>', re.DOTALL)
new_backups = """<section id="backups-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg>
                <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Backups</h2>
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                    Create backup
                </button>
            </div>
        </div>
        
        <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; padding: 40px; text-align: center;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
            <div style="color: #6b7280; font-size: 14px;">No backups created yet.</div>
        </div>
    </div>
</section>"""
content = backups_pattern.sub(new_backups, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed fake HTML blocks.")
