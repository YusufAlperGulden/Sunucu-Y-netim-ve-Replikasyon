import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Prepare new changelog item
new_item = """
                <div class="changelog-item">
                    <div class="changelog-date">August 19, 2026</div>
                    <div class="changelog-title">User Management UI Implemented</div>
                    <ul class="changelog-list">
                        <li>Fixed the 'User management' sidebar link which was previously unclickable.</li>
                        <li>Implemented the User Management interface structure including Users, Teams, and LDAP tabs.</li>
                        <li>Added the 'Create user or team' modal dialog.</li>
                        <li>Note: No fake users have been populated in accordance with the real-data guidelines.</li>
                    </ul>
                </div>
"""

# Insert right after <div class="changelog-content">
pattern = r'(<div class="changelog-content">)'
content = re.sub(pattern, r'\1' + new_item, content, count=1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated")
