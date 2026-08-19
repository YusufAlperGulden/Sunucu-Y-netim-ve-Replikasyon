import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

recent_alarms_pattern = r'<div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; color: var\(--text-muted\); font-size: 0\.95rem;">\s*<svg[^>]+>.*?</svg>\s*No alarms\s*</div>'

new_recent_alarms = """<div id="recent-alarms-container" style="flex: 1; display: flex; flex-direction: column; overflow-y: auto; padding: 16px;">
                              <div style="display:flex; align-items:center; justify-content:center; height:100%; color: var(--text-muted); font-size: 0.95rem;">
                                  Loading alarms...
                              </div>
                          </div>"""

if "recent-alarms-container" not in content:
    content = re.sub(recent_alarms_pattern, new_recent_alarms, content, flags=re.DOTALL)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added recent-alarms-container to index.html")
else:
    print("recent-alarms-container already exists")
