import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix sidebar link
old_backups_link = """<a href="#">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg> <span class="sidebar-text">Backups</span>
                </a>"""
new_backups_link = """<a href="#" class="sidebar-link" data-view="backups-view">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg> <span class="sidebar-text">Backups</span>
                </a>"""
content = content.replace(old_backups_link, new_backups_link)

# Add backups-view
backups_view = """
        <!-- BACKUPS VIEW -->
        <section id="backups-view" class="view-section" style="display: none;">
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
                        <button style="background: white; border: 1px solid var(--border); border-radius: 6px; padding: 0 12px; display: flex; align-items: center; cursor: pointer; color: #4b5563;">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                        </button>
                    </div>
                </div>
                
                <div style="background: white; margin-bottom: 24px; padding-right: 20px; display: flex; justify-content: flex-end;">
                    <button style="background: white; border: 1px solid var(--border); border-radius: 6px; padding: 6px 12px; display: flex; align-items: center; gap: 8px; cursor: pointer; color: #4b5563; font-size: 0.85rem; font-weight: 500;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                        View
                    </button>
                </div>

                <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; border-bottom: 1px solid var(--border); padding: 0 20px;">
                        <button class="tab-btn active" id="tab-btn-all-backups" style="padding: 16px 20px; font-weight: 500; color: #3a1c94; border-bottom: 2px solid #3a1c94; font-size: 0.95rem; background: none; border-top: none; border-left: none; border-right: none; cursor: pointer;">All Backups</button>
                        <button class="tab-btn" id="tab-btn-schedules" style="padding: 16px 20px; font-weight: 500; color: #4b5563; font-size: 0.95rem; background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer;">Schedules</button>
                    </div>
                    
                    <div id="content-all-backups" style="display: block; overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; min-width: 1000px;">
                            <thead>
                                <tr style="border-bottom: 1px solid var(--glass-border); background: #ffffff;">
                                    <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">ID <span style="font-size: 0.7rem; color: #3a1c94;">&#9660;</span></th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Info</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Cluster</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                                        Method
                                    </th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Status</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Title</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Created <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-left: 4px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg></th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Size</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Backup host</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Storage</th>
                                    <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="all-backups-tbody">
                                <!-- JS Injected -->
                            </tbody>
                        </table>
                    </div>

                    <div id="content-schedules" style="display: none; overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; min-width: 1000px;">
                            <thead>
                                <tr style="border-bottom: 1px solid var(--glass-border); background: #ffffff;">
                                    <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Name</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Cluster</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                                        Method
                                    </th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Status</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Schedule</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Backup Host</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Storage Host</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Storage Location</th>
                                    <th style="padding: 12px 10px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Last Execution</th>
                                    <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #4b5563;">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="schedules-tbody">
                                <!-- JS Injected -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
"""

content = content.replace('<!-- CHANGELOG VIEW -->', backups_view + '\n        <!-- CHANGELOG VIEW -->')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML updated.")
