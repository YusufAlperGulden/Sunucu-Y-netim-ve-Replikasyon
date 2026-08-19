import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

reports_view_pattern = r'<section id="reports-view" class="view-section" style="display: none;">\s*<div style="padding: 24px;">.*?</div>\s*</section>'

new_reports_view = """<section id="reports-view" class="view-section" style="display: none;">
      <div style="padding: 24px;">
          <!-- Header -->
          <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="8" y1="8" x2="16" y2="8"></line><line x1="8" y1="12" x2="16" y2="12"></line><line x1="8" y1="16" x2="12" y2="16"></line></svg>
              <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Operational reports</h2>
          </div>
          
          <!-- Content Card -->
          <div class="glass-panel" style="background: white; border: 1px solid var(--border); border-radius: 12px; padding: 24px;">
              
              <!-- Tabs -->
              <div style="display: flex; gap: 24px; border-bottom: 1px solid var(--glass-border); margin-bottom: 20px;">
                  <div id="tab-reports-sub" onclick="switchReportsTab('reports')" style="padding-bottom: 12px; cursor: pointer; color: var(--primary); font-weight: 500; border-bottom: 2px solid var(--primary); font-size: 0.9rem;">Reports</div>
                  <div id="tab-schedules-sub" onclick="switchReportsTab('schedules')" style="padding-bottom: 12px; cursor: pointer; color: var(--text-muted); font-weight: 500; border-bottom: 2px solid transparent; font-size: 0.9rem;">Schedules</div>
              </div>

              <!-- Actions row -->
              <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                  <button id="btn-create-report-action" class="btn-primary" style="display: flex; align-items: center; gap: 8px; border-radius: 20px; padding: 8px 16px;" onclick="document.getElementById('modal-create-report').style.display='flex'">
                      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                      <span id="text-create-report-action">Create report</span>
                  </button>
              </div>

              <!-- Reports Table -->
              <div id="table-reports" style="display: block;">
                  <table style="width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 40px;">
                      <thead style="background: white; border-bottom: 1px solid var(--border);">
                          <tr>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Created</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">File name</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Report type</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Cluster</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Created by</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Data range</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Recipients</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Actions</th>
                          </tr>
                      </thead>
                      <tbody>
                      </tbody>
                  </table>
                  <div style="text-align: center; color: #6b7280; font-size: 14px; padding: 20px;">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 10px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                      No reports generated yet <span style="font-size: 0.65rem; color: #ef4444; font-weight: bold; margin-left: 5px;">[PLACEHOLDER]</span>
                  </div>
              </div>

              <!-- Schedules Table -->
              <div id="table-schedules" style="display: none;">
                  <table style="width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 40px;">
                      <thead style="background: white; border-bottom: 1px solid var(--border);">
                          <tr>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Schedule</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Report type</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Cluster</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Data range</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Recipients</th>
                              <th style="padding: 12px 0; font-weight: 600; font-size: 0.8rem; color: #374151;">Actions</th>
                          </tr>
                      </thead>
                      <tbody>
                      </tbody>
                  </table>
                  <div style="text-align: center; color: #6b7280; font-size: 14px; padding: 20px;">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="2" style="margin: 0 auto 10px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                      No schedules generated yet <span style="font-size: 0.65rem; color: #ef4444; font-weight: bold; margin-left: 5px;">[PLACEHOLDER]</span>
                  </div>
              </div>

          </div>
      </div>
  </section>"""

if re.search(reports_view_pattern, content, flags=re.DOTALL):
    content = re.sub(reports_view_pattern, new_reports_view, content, flags=re.DOTALL)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced reports-view successfully.")
else:
    print("Could not find reports-view section.")
