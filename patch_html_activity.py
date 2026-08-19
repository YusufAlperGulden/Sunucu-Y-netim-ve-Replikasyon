import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

empty_activity = """<div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px; padding: 40px; text-align: center;">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
              <div style="color: #6b7280; font-size: 14px;">No activities or alarms recorded yet.</div>
          </div>"""

activity_table = """<div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px;">
              <table style="width: 100%; border-collapse: collapse;">
                  <thead style="background: #f9fafb; border-bottom: 1px solid var(--border);">
                      <tr>
                          <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 500; color: #6b7280; text-transform: uppercase;">Date</th>
                          <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 500; color: #6b7280; text-transform: uppercase;">User</th>
                          <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 500; color: #6b7280; text-transform: uppercase;">Action</th>
                          <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 500; color: #6b7280; text-transform: uppercase;">Details</th>
                      </tr>
                  </thead>
                  <tbody id="activity-tbody">
                      <tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">Loading activity logs...</td></tr>
                  </tbody>
              </table>
          </div>"""

if empty_activity in content:
    content = content.replace(empty_activity, activity_table)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced Activity Center empty state with table")
else:
    print("Empty activity HTML not found")
