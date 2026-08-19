import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Teams and LDAP tabs
content = re.sub(r'<div id="tab-btn-teams".*?</div>', '', content)
content = re.sub(r'<div id="tab-btn-ldap".*?</div>', '', content)

# Remove their content sections
content = re.sub(r'<!-- TEAMS TABLE -->[\s\S]*?<!-- LDAP TABLE -->', '<!-- LDAP TABLE -->', content)
content = re.sub(r'<!-- LDAP TABLE -->[\s\S]*?</div>\s*</div>\s*</section>', '</div>\n        </div>\n        </section>', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed Teams and LDAP from UI")
