with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

backup_tab_js = """
    window.switchBackupTab = function(tabName) {
        document.querySelectorAll('.backup-tab').forEach(el => {
            el.style.color = '#6b7280';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active-tab');
        });
        document.querySelectorAll('.backup-tab-content').forEach(el => el.style.display = 'none');
        
        if (tabName === 'all') {
            const tabAll = document.getElementById('tab-all-backups');
            if (tabAll) {
                tabAll.style.color = 'var(--primary)';
                tabAll.style.borderBottom = '2px solid var(--primary)';
                tabAll.classList.add('active-tab');
            }
            const contentAll = document.getElementById('content-all-backups');
            if (contentAll) contentAll.style.display = 'block';
        } else if (tabName === 'schedules') {
            const tabSched = document.getElementById('tab-schedules-backups');
            if (tabSched) {
                tabSched.style.color = 'var(--primary)';
                tabSched.style.borderBottom = '2px solid var(--primary)';
                tabSched.classList.add('active-tab');
            }
            const contentSched = document.getElementById('content-schedules-backups');
            if (contentSched) contentSched.style.display = 'block';
        }
    };
"""

if 'window.switchBackupTab' not in js:
    js = js + "\n\n" + backup_tab_js

# Update Changelog anchors and asset version
js = js.replace("changelogAnchors = ['v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=62', 'v=63')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with switchBackupTab and v1.5.6 (v63)")
