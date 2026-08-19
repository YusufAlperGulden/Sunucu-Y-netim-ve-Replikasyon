import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Prepare new changelog item
new_item = """
                <div class="changelog-item">
                    <div class="changelog-date">August 19, 2026</div>
                    <div class="changelog-title">UI Stability and Authentication Flow Fixes</div>
                    <ul class="changelog-list">
                        <li>Fixed a bug where API session timeouts (401 Unauthorized) would wipe out dashboard components and cause JavaScript errors.</li>
                        <li>Added robust safety guards across the dashboard to prevent "null reference" crashes when rendering metrics.</li>
                        <li>Improved the Login screen overlay to properly obscure the dashboard interface when a session expires.</li>
                        <li>Restored the top announcement banner container for upcoming custom messaging.</li>
                    </ul>
                </div>
"""

# Insert right after <div class="changelog-content">
pattern = r'(<div class="changelog-content">)'
content = re.sub(pattern, r'\1' + new_item, content, count=1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated")
