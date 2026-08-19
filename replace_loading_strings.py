js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

LOADING_HTML = '<div style=\\"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:60px 20px;\\"><div class=\\"cc-spinner cc-spinner-lg\\"></div><span style=\\"color:#9ca3af;font-size:0.85rem;\\">Yukleniyor...</span></div>'
LOADING_TD_HTML = f'<tr class=\\"cc-loading-row\\"><td colspan=\\"10\\"><div style=\\"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;\\"><div class=\\"cc-spinner cc-spinner-lg\\"></div><span style=\\"color:#9ca3af;font-size:0.85rem;\\">Yukleniyor...</span></div></td></tr>'

# Replace loading strings in fetchNodesPage
replacements = [
    # Nodes page loading row
    ("'<tr><td colspan=\"10\" style=\"text-align:center;padding:30px;color:#9ca3af;\">Yukleniyor...</td></tr>'",
     f"'<tr class=\"cc-loading-row\"><td colspan=\"10\"><div style=\"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;\"><div class=\"cc-spinner cc-spinner-lg\"></div><span style=\"color:#9ca3af;font-size:0.85rem;\">Yukleniyor...</span></div></td></tr>'"),
    # Projects loading  
    ("'<tr><td colspan=\"4\" style=\"text-align:center; padding: 20px; color: #6b7280;\">Loading activity logs...</td></tr>'",
     "'<tr class=\"cc-loading-row\"><td colspan=\"4\"><div style=\"display:flex;flex-direction:column;align-items:center;gap:12px;\"><div class=\"cc-spinner\"></div><span style=\"color:#9ca3af;\">Yukleniyor...</span></div></td></tr>'"),
    # Audit log
    ("'<tr><td colspan=\"4\" style=\"text-align:center; padding: 20px; color: #6b7280;\">Yükleniyor...</td></tr>'",
     "'<tr class=\"cc-loading-row\"><td colspan=\"4\"><div style=\"display:flex;flex-direction:column;align-items:center;gap:12px;\"><div class=\"cc-spinner\"></div><span style=\"color:#9ca3af;\">Yukleniyor...</span></div></td></tr>'"),
    # Jobs tab
    ("tbody.innerHTML = '<tr><td colspan=\"7\" style=\"text-align:center;padding:40px;color:#9ca3af;\">Yukleniyor...</td></tr>';",
     "tbody.innerHTML = '<tr class=\"cc-loading-row\"><td colspan=\"7\"><div style=\"display:flex;flex-direction:column;align-items:center;gap:12px;\"><div class=\"cc-spinner\"></div><span style=\"color:#9ca3af;\">Yukleniyor...</span></div></td></tr>';"),
    # Inline loading text
    ("'<tr><td colspan=\"9\" style=\"text-align:center; padding: 20px; color: #6b7280;\">Yükleniyor...</td></tr>'",
     "'<tr class=\"cc-loading-row\"><td colspan=\"9\"><div style=\"display:flex;flex-direction:column;align-items:center;gap:12px;\"><div class=\"cc-spinner\"></div><span style=\"color:#9ca3af;\">Yukleniyor...</span></div></td></tr>'"),
]

count = 0
for old, new in replacements:
    if old in js:
        js = js.replace(old, new)
        count += 1
    else:
        print(f"NOT FOUND: {old[:80]}")

print(f"Replaced {count} loading strings")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
