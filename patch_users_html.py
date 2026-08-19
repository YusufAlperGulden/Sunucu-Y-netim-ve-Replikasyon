# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<a href="#">\n                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><path d="M11.5 15H7a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M21.378 10.626a1 1 0 1 0-3.004-3.004l-4.01 4.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"></path></svg> <span class="sidebar-text">User management</span>\n                  </a>',
    '<a href="#" class="sidebar-link" data-view="users-view">\n                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><path d="M11.5 15H7a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M21.378 10.626a1 1 0 1 0-3.004-3.004l-4.01 4.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"></path></svg> <span class="sidebar-text">User management</span>\n                  </a>'
)

users_view = """
      <!-- USERS VIEW -->
      <section id="users-view" class="view-section" style="display: none;">
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
              
              <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                  <div style="display: flex; border-bottom: 1px solid var(--border); padding: 0 20px;">
                      <button class="tab-btn active" id="tab-btn-users" style="padding: 16px 20px; font-weight: 500; color: var(--primary); border-bottom: 2px solid var(--primary); font-size: 0.95rem; background: none; border: none; cursor: pointer;">Users</button>
                      <button class="tab-btn" id="tab-btn-teams" style="padding: 16px 20px; font-weight: 500; color: #4b5563; font-size: 0.95rem; background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer;">Teams</button>
                      <button class="tab-btn" id="tab-btn-ldap" style="padding: 16px 20px; font-weight: 500; color: #4b5563; font-size: 0.95rem; background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer;">LDAP</button>
                  </div>
                  
                  <div id="content-users" style="display: block;">
                      <table style="width: 100%; border-collapse: collapse; text-align: left;">
                          <thead>
                              <tr style="border-bottom: 1px solid var(--glass-border); background: #f9fafb;">
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 25%; position: relative; cursor: pointer; user-select: none;" id="th-user-col">
                                      User <span class="sort-icon" style="font-size: 0.7rem; margin-left: 4px; color: #a0aec0;" id="user-sort-arrows">&#9650;&#9660;</span>
                                      <!-- Sort Tooltip -->
                                      <div id="user-sort-tooltip" style="display: none; position: absolute; background: #111827; color: white; padding: 6px 10px; border-radius: 6px; font-size: 0.75rem; white-space: nowrap; top: -25px; left: 24px; z-index: 100;">
                                          Click to sort ascending
                                          <!-- Arrow pointing down for tooltip -->
                                          <div style="position: absolute; bottom: -4px; left: 16px; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 4px solid #111827;"></div>
                                      </div>
                                  </th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 20%;">Email</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 10%;">Team</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 10%;">First name</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 10%;">Last name</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 10%;">Status</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 10%;">Created</th>
                                  <th style="padding: 12px 24px; font-weight: 600; font-size: 0.85rem; color: #6b7280; width: 5%;">Actions</th>
                              </tr>
                          </thead>
                          <tbody id="users-tbody">
                              <!-- Rows injected via JS -->
                          </tbody>
                      </table>
                  </div>
                  
                  <div id="content-teams" style="display: none;">
                      <div style="padding: 40px; text-align: center; color: var(--text-muted);">Teams content not implemented in this demo.</div>
                  </div>
                  
                  <div id="content-ldap" style="display: none;">
                      <div style="padding: 40px; text-align: center; color: var(--text-muted);">LDAP content not implemented in this demo.</div>
                  </div>
              </div>
          </div>
      </section>
"""

content = content.replace("</main>", users_view + "\n        </main>")

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML patched")
