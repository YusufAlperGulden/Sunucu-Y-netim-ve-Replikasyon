import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the whole <section id="activity-view">
pattern = r'<section id="activity-view" class="view-section" style="display: none;">.*?</section>'

new_section = """<section id="activity-view" class="view-section" style="display: none;">
      <div style="padding: 24px;">
          <div class="glass-panel" style="padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; border: 1px solid var(--border); background: white; border-radius: 12px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 16px;"><path d="M19 3H5C3.9 3 3 3.9 3 5v14c0 1.1.9 2 2 2h7"></path><path d="M3 16l4-4 4 4"></path><path d="M8 11l3-3 3 3"></path><path d="M22 17c0 0-1.5-2.5-4-2.5S14 17 14 17s1.5 2.5 4 2.5S22 17 22 17z"></path><circle cx="18" cy="17" r="1"></circle></svg>
              <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Activity center</h2>
          </div>
          
          <div class="glass-panel" style="background: white; border: 1px solid var(--border); overflow: hidden; border-radius: 12px;">
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
          </div>
      </div>
  </section>"""

content = re.sub(pattern, new_section, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced section activity-view")
