import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

AUDIT_TAB_HTML = """      <!-- AUDIT LOG Tab -->
      <div id="ac-content-audit" style="display: block; padding: 0;">
        <!-- Control Bar: Search, Date Filter, Refresh, Export CSV -->
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid #e5e7eb; gap: 12px; flex-wrap: wrap;">
          <!-- Left: Search Box and Date Range -->
          <div style="display: flex; align-items: center; gap: 12px; flex: 1; max-width: 600px;">
            <!-- Search Box with Magnifying Glass & Clear Icon -->
            <div style="position: relative; flex: 1; min-width: 220px;">
              <input type="text" id="audit-search-input" placeholder="Search message or hostname..." oninput="window.filterAuditLogs()"
                style="width: 100%; padding: 8px 36px 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.85rem; outline: none; background: white; transition: border-color 0.2s;"
                onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='#d1d5db'">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); pointer-events: none;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            
            <!-- Date Range Picker Placeholder -->
            <div style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; border: 1px solid #e5e7eb; border-radius: 6px; background: #f9fafb; color: #9ca3af; font-size: 0.85rem; user-select: none;">
              <span>Start date</span>
              <span>&rarr;</span>
              <span>End date</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left: 6px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            </div>
          </div>

          <!-- Right: Refresh & Export CSV Buttons -->
          <div style="display: flex; align-items: center; gap: 8px;">
            <!-- Refresh Button -->
            <button onclick="window.fetchAuditLogs()" title="Refresh" id="btn-refresh-audit"
              style="display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border: 1px solid #d1d5db; border-radius: 6px; background: white; cursor: pointer; color: #4b5563; transition: all 0.2s;"
              onmouseenter="this.style.background='#f9fafb'" onmouseleave="this.style.background='white'">
              <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
            </button>
            
            <!-- Export CSV Button -->
            <button onclick="window.exportAuditLogsCsv()" id="btn-export-audit"
              style="display: flex; align-items: center; gap: 6px; padding: 7px 14px; border: 1px solid #d1d5db; border-radius: 6px; background: white; cursor: pointer; font-size: 0.85rem; font-weight: 500; color: #374151; transition: all 0.2s;"
              onmouseenter="this.style.background='#f9fafb'" onmouseleave="this.style.background='white'">
              <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              Export CSV
            </button>
          </div>
        </div>

        <table style="width: 100%; border-collapse: collapse;">
          <thead style="background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
            <tr>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">When</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">Activity</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">Type</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">User</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">Hostname</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151; white-space: nowrap;">Cluster Name</th>
            </tr>
          </thead>
          <tbody id="activity-tbody"><tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading activity logs...</span></div></td></tr></tbody>
        </table>
      </div>"""

# Replace in index.html
start_idx = html.find('<!-- AUDIT LOG Tab -->')
end_idx = html.find('<!-- WATCHLISTS Tab -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + AUDIT_TAB_HTML + "\n\n      " + html[end_idx:]
    print("Replaced AUDIT LOG Tab HTML successfully")
else:
    print("Could not find start/end markers:", start_idx, end_idx)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
