import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract everything between <section id="users-view"...> and </section>
pattern_section = r'(<section id="users-view".*?>).*?(</section>)'

new_section_content = """
      <div style="padding: 24px;">
          <!-- Top Header -->
          <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px;">
              <div style="display: flex; align-items: center;">
                  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><path d="M11.5 15H7a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M21.378 10.626a1 1 0 1 0-3.004-3.004l-4.01 4.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"></path></svg>
                  <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">User management</h2>
              </div>
              <button class="btn-primary" style="display: flex; align-items: center; gap: 8px; border-radius: 20px; padding: 8px 16px;" onclick="document.getElementById('modal-create-user-team').style.display='flex'">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                  Create user or team
              </button>
          </div>
          
          <!-- Tabs and Content Area -->
          <div class="glass-panel" style="background: white; border: 1px solid var(--border); border-radius: 12px; padding: 24px;">
              
              <!-- Tabs -->
              <div style="display: flex; gap: 24px; border-bottom: 1px solid var(--glass-border); margin-bottom: 24px;">
                  <div id="tab-users" class="user-tab active-tab" onclick="switchUserTab('users')" style="padding-bottom: 12px; cursor: pointer; color: var(--primary); font-weight: 500; border-bottom: 2px solid var(--primary);">Users</div>
                  <div id="tab-teams" class="user-tab" onclick="switchUserTab('teams')" style="padding-bottom: 12px; cursor: pointer; color: var(--text-muted); font-weight: 500; border-bottom: 2px solid transparent;">Teams</div>
                  <div id="tab-ldap" class="user-tab" onclick="switchUserTab('ldap')" style="padding-bottom: 12px; cursor: pointer; color: var(--text-muted); font-weight: 500; border-bottom: 2px solid transparent;">LDAP</div>
              </div>

              <!-- USERS TABLE -->
              <div id="content-users" class="user-tab-content">
                  <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                      <thead>
                          <tr style="border-bottom: 1px solid var(--glass-border); color: var(--text-muted); text-align: left;">
                              <th style="padding: 12px 16px; font-weight: 600;">User <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Email <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Team <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">First name <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Last name <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Status <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600;">Created <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600; text-align: right;">Actions</th>
                          </tr>
                      </thead>
                      <tbody>
                          <tr>
                              <td colspan="8" style="padding: 40px; text-align: center; color: var(--text-muted);">
                                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 16px auto; display: block;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                                  No users created yet.
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>

              <!-- TEAMS TABLE -->
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

              <!-- LDAP TABLE -->
              <div id="content-ldap" class="user-tab-content" style="display: none;">
                  <div style="display: flex; gap: 24px; margin-bottom: 24px;">
                      <a href="#" style="color: var(--primary); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 8px;">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg> Map LDAP group
                      </a>
                      <a href="#" style="color: var(--primary); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 8px;">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg> LDAP Settings
                      </a>
                  </div>
                  <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                      <thead>
                          <tr style="border-bottom: 1px solid var(--glass-border); color: var(--text-muted); text-align: left;">
                              <th style="padding: 12px 16px; font-weight: 600;">LDAP Group <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-left:4px;"><polyline points="7 14 12 19 17 14"></polyline><polyline points="7 10 12 5 17 10"></polyline></svg></th>
                              <th style="padding: 12px 16px; font-weight: 600; text-align: right;">Actions</th>
                          </tr>
                      </thead>
                      <tbody>
                          <tr>
                              <td colspan="2" style="padding: 40px; text-align: center; color: var(--text-muted);">
                                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 16px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                                  No LDAP groups mapped yet.
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>

          </div>
      </div>
"""

content = re.sub(pattern_section, r'\1' + new_section_content + r'\2', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated users view")
