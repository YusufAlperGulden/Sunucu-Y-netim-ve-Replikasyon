import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract dashboard-view content
dashboard_view_match = re.search(r'<!-- DASHBOARD VIEW -->\s*<div id="dashboard-view" class="view-section" style="display: none;">(.*?)</div>\s*<!-- SETTINGS VIEW -->', content, re.DOTALL)
if not dashboard_view_match:
    print("Could not find dashboard-view")
    exit(1)

dashboard_content = dashboard_view_match.group(1).strip()

# Remove the top-level dashboard-view entirely
content = content.replace(dashboard_view_match.group(0), '<!-- SETTINGS VIEW -->')

# 2. Insert it into tab-content-dashboards
tab_content_start = '<div id="tab-content-dashboards" class="tab-content active">'

# Find where to insert it. We'll insert it right after the header of tab-content-dashboards.
# Actually, let's just insert it right after the `<div id="tab-content-dashboards" class="tab-content active">`
new_dashboard_html = f"""
{tab_content_start}
    <div style="margin-bottom: 24px; background: white; border: 1px solid var(--border); border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        {dashboard_content}
    </div>
"""

content = content.replace(tab_content_start, new_dashboard_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Moved dashboard-view into tab-content-dashboards")
