with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Backups section
old_backups_section = """        <!-- BACKUPS VIEW -->
        <section id="backups-view" class="view-section" style="display: none;">
    <div style="padding: 24px;">
        <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg>
                <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Backups</h2>
            </div>
            <div style="display: flex; gap: 8px;">
                <button id="btn-global-create-backup" class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px;">
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

new_backups_section = """        <!-- BACKUPS VIEW -->
        <section id="backups-view" class="view-section" style="display: none;">
            <div style="padding: 24px;">
                <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg>
                        <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Backups</h2>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button id="btn-global-create-backup" class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px; border-radius: 6px; padding: 8px 16px; font-weight: 500;">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                            Create backup
                        </button>
                    </div>
                </div>
                
                <!-- Backups Folders Card -->
                <div class="glass-panel" style="background: white; border: 1px solid var(--border); border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    
                    <!-- Tabs -->
                    <div style="display: flex; gap: 24px; border-bottom: 1px solid var(--border); margin-bottom: 24px;">
                        <div id="tab-all-backups" class="backup-tab active-tab" onclick="window.switchBackupTab('all')" style="padding-bottom: 12px; cursor: pointer; color: var(--primary); font-weight: 600; border-bottom: 2px solid var(--primary); font-size: 0.95rem;">All Backups</div>
                        <div id="tab-schedules-backups" class="backup-tab" onclick="window.switchBackupTab('schedules')" style="padding-bottom: 12px; cursor: pointer; color: #6b7280; font-weight: 500; border-bottom: 2px solid transparent; font-size: 0.95rem;">Schedules</div>
                    </div>

                    <!-- FOLDER 1: ALL BACKUPS TABLE -->
                    <div id="content-all-backups" class="backup-tab-content">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead>
                                <tr style="border-bottom: 1px solid var(--border); color: #6b7280; text-align: left; background: #fafafa;">
                                    <th style="padding: 12px 16px; font-weight: 600;">ID <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Info</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Cluster</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Method</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Status</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Title</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Created</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Size</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Backup host</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Storage</th>
                                    <th style="padding: 12px 16px; font-weight: 600; text-align: right;">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="11" style="padding: 60px 20px; text-align: center; color: #6b7280;">
                                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="margin: 0 auto 16px auto; display: block;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                        No backups created yet.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- FOLDER 2: SCHEDULES TABLE -->
                    <div id="content-schedules-backups" class="backup-tab-content" style="display: none;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead>
                                <tr style="border-bottom: 1px solid var(--border); color: #6b7280; text-align: left; background: #fafafa;">
                                    <th style="padding: 12px 16px; font-weight: 600;">ID <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Cluster</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Schedule</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Method</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Next Run</th>
                                    <th style="padding: 12px 16px; font-weight: 600;">Status</th>
                                    <th style="padding: 12px 16px; font-weight: 600; text-align: right;">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="7" style="padding: 60px 20px; text-align: center; color: #6b7280;">
                                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="margin: 0 auto 16px auto; display: block;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line><path d="M12 14v4"></path><path d="M10 16h4"></path></svg>
                                        No schedules created yet.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                </div>
            </div>
        </section>"""

if old_backups_section in html:
    html = html.replace(old_backups_section, new_backups_section, 1)
    print("Replaced Backups section HTML")
else:
    idx_b = html.find('id="backups-view"')
    idx_b_end = html.find('id="changelog-view"', idx_b)
    html = html[:idx_b-25] + new_backups_section + "\n\n        " + html[idx_b_end-25:]
    print("Replaced Backups section by index range")

# 2. Make Backup Modals Solid White Background
html = html.replace('<div class="modal-content" style="max-width: 700px; width: 100%; padding: 40px; border-radius: 12px;">', '<div class="modal-content" style="max-width: 700px; width: 100%; padding: 40px; border-radius: 12px; background: #ffffff; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15), 0 10px 10px -5px rgba(0,0,0,0.04); border: 1px solid #e5e7eb;">')
html = html.replace('<div class="modal-content" style="max-width: 800px; width: 100%; border-radius: 12px; padding: 0; display: flex; flex-direction: column;">', '<div class="modal-content" style="max-width: 800px; width: 100%; border-radius: 12px; padding: 0; display: flex; flex-direction: column; background: #ffffff; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15), 0 10px 10px -5px rgba(0,0,0,0.04); border: 1px solid #e5e7eb;">')

# 3. Update Changelog for v1.5.6
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.5 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.4</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.6 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.5</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.4</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.5 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.4 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.6 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.5 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.4 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

old_content_top = """                    <h2 id="v1-5-5" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.5</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Visual Design (Larger Floating Bubbles):</span> Giriş ekranındaki (Login screen) hareketli baloncuklar (floating bubbles) daha büyük, canlı ve estetik boyutlara yükseltildi (120px - 340px yarıçap). Yumuşak geçişler ve şeffaf katman efektleri uygulandı.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-6" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.6</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (Backups Folders &amp; Solid White Modals):</span> Backups sayfasına ClusterControl standardında iki klasör sekmesi eklendi: <code>All Backups</code> (<code>No backups created yet.</code>) ve <code>Schedules</code> (<code>No schedules created yet.</code>). Ayrıca yedekleme sihirbazı ve seçim pencerelerinin arka planı şeffaf/gri görünümden arındırılarak saf beyaz (solid white) kurumsal modal tasarımına dönüştürüldü.</li>
                    </ul>

                    <h2 id="v1-5-5" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.5</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Visual Design (Larger Floating Bubbles):</span> Giriş ekranındaki (Login screen) hareketli baloncuklar (floating bubbles) daha büyük, canlı ve estetik boyutlara yükseltildi (120px - 340px yarıçap). Yumuşak geçişler ve şeffaf katman efektleri uygulandı.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=63
html = html.replace('v=62', 'v=63')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Backups tabs, solid white modals, and v1.5.6 (v63)")
