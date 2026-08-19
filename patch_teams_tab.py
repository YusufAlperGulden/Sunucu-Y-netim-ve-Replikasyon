with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Teams and LDAP content blocks inside User management
teams_and_ldap_html = """              <!-- TEAMS TABLE -->
              <div id="content-teams" class="user-tab-content" style="display: none;">
                  <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                      <thead>
                          <tr style="border-bottom: 1px solid var(--glass-border); color: var(--text-muted); text-align: left;">
                              <th style="padding: 12px 16px; font-weight: 600;">Name <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Owner <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Created <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600; text-align: right;">Actions</th>
                          </tr>
                      </thead>
                      <tbody>
                          <tr>
                              <td colspan="4" style="padding: 40px; text-align: center; color: var(--text-muted);">
                                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 16px auto; display: block;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                                  No teams created yet.
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>

              <!-- LDAP TAB -->
              <div id="content-ldap" class="user-tab-content" style="display: none;">
                  <div style="padding: 40px; text-align: center; color: var(--text-muted);">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 16px auto; display: block;"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>
                      No LDAP configurations created yet.
                  </div>
              </div>"""

users_table_end = html.find('</div>\n\n              </div>\n        </div>\n        </section>')
if users_table_end == -1:
    users_table_end = html.find('</div>\n\n              </div>\n        </div>\n        </section>')
if users_table_end == -1:
    idx_u = html.find('id="content-users"')
    idx_u_close = html.find('</div>', idx_u + 500)
    html = html[:idx_u_close+6] + "\n\n" + teams_and_ldap_html + html[idx_u_close+6:]
    print("Inserted teams_and_ldap_html after content-users")
else:
    html = html[:users_table_end] + "\n\n" + teams_and_ldap_html + html[users_table_end:]
    print("Inserted teams_and_ldap_html")

# 2. Update Left Sidebar in Changelog for v1.4.8
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.7 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.6</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.8 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.7</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.6</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.4.8 (Latest)")

# 3. Update TOC for v1.4.8
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.7 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.6 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.8 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.7 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.6 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.4.8 Release")

# 4. Update Middle Content for v1.4.8
old_content_top = """                    <h2 id="v1-4-7" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.7</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Detail Nodes Tab):</span> Cluster Detay sayfasındaki Nodes sekmesinde düğüm sayısı kartlarının <code>0</code> olarak görünmesine sebep olan DOM ID çakışması giderildi (<code>cluster-stat-*</code>). Artık seçili cluster'a ait tüm düğümler anında <code>Operational: 2</code>, <code>All: 2</code> vb. olarak dinamik şekilde kartlara yansıtılmaktadır.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-4-8" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.8</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (User Management - Teams Tab):</span> User Management ekranına <b>Teams</b> sekmesi tablosu eklendi. "Name", "Owner", "Created", "Actions" sütun başlıkları ve standart boş durum mesajı (<code>No teams created yet.</code>) eklendi.</li>
                    </ul>

                    <h2 id="v1-4-7" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.7</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Detail Nodes Tab):</span> Cluster Detay sayfasındaki Nodes sekmesinde düğüm sayısı kartlarının <code>0</code> olarak görünmesine sebep olan DOM ID çakışması giderildi (<code>cluster-stat-*</code>). Artık seçili cluster'a ait tüm düğümler anında <code>Operational: 2</code>, <code>All: 2</code> vb. olarak dinamik şekilde kartlara yansıtılmaktadır.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.4.8")

# Bump asset version to v=55
html = html.replace('v=54', 'v=55')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("changelogAnchors = ['v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=54', 'v=55')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with v1.4.8 anchor and v=55")
