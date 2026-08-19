import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the stats row
old_stats = r'<div style="display: flex; gap: 10px; margin-bottom: 20px; overflow-x: auto;">.*?</div>\s*</div>\s*<div style="overflow-x: auto;">'

new_stats = """<div style="display: flex; margin-bottom: 20px; border: 1px solid var(--border); border-radius: 4px; overflow-x: auto; background: white;">
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border); border-left: 2px solid #10b981;">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Operational</div>
                              <div style="color: #10b981; font-size: 24px;" id="stat-operational">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border); border-top: 1px solid transparent; border-bottom: 1px solid transparent;">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Failed</div>
                              <div style="color: #374151; font-size: 24px;" id="stat-failed">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border);">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Offline</div>
                              <div style="color: #374151; font-size: 24px;" id="stat-offline">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border);">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Shut Down</div>
                              <div style="color: #3b82f6; font-size: 24px;" id="stat-shutdown">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border);">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Recovering</div>
                              <div style="color: #374151; font-size: 24px;" id="stat-recovering">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border-right: 1px solid var(--border);">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">Unknown State</div>
                              <div style="color: #374151; font-size: 24px;" id="stat-unknown">0</div>
                          </div>
                          <div style="flex: 1; min-width: 120px; padding: 15px 20px; border: 1px solid #8b5cf6;">
                              <div style="color: #6b7280; font-size: 13px; margin-bottom: 5px;">All</div>
                              <div style="color: #374151; font-size: 24px;" id="stat-all">0</div>
                          </div>
                      </div>
                      
                      <div style="display: flex; justify-content: flex-end; margin-bottom: 15px;">
                          <button style="display: flex; align-items: center; gap: 6px; padding: 6px 16px; background: white; border: 1px solid var(--border); border-radius: 4px; font-size: 13px; cursor: pointer; color: #374151; font-weight: 500;"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg> View</button>
                      </div>

                      <div style="overflow-x: auto;">"""

content = re.sub(old_stats, new_stats, content, flags=re.DOTALL)

# Add Last seen and Actions columns to the table
old_th = r'<th style="padding: 10px 0; font-weight: 500;">Version</th>\s*</tr>'
new_th = """<th style="padding: 10px 0; font-weight: 500;">Version</th>
                                      <th style="padding: 10px 0; font-weight: 500;">Last seen</th>
                                      <th style="padding: 10px 0; font-weight: 500; text-align: center;">Actions</th>
                                  </tr>"""
content = re.sub(old_th, new_th, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML for node list")
