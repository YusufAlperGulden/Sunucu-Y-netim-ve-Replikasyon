import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the stray offline lines that write m.uptime and m.plates as undefined
old_stray = """{ const TMP_EL = document.getElementById("metric-" + node.id + "-uptime"); if(TMP_EL) {                         TMP_EL.innerText = m.uptime; } }
{ const TMP_EL = document.getElementById("metric-" + node.id + "-plates"); if(TMP_EL) {                         TMP_EL.innerText = m.plates; } }
                    } else {"""

new_stray = """
                      // Show error reason under the offline badge
                      const errEl = document.getElementById("metric-" + node.id + "-status");
                      if(errEl && m.error) errEl.title = m.error;
                    } else {"""

if 'TMP_EL.innerText = m.uptime; } }\n{ const TMP_EL = document.getElementById("metric-" + node.id + "-plates"); if(TMP_EL) {                         TMP_EL.innerText = m.plates; } }' in content:
    content = content.replace(old_stray, new_stray)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed stray offline lines causing undefined")
else:
    print("Pattern not found exactly, trying alternative...")
    # Try to find and remove just those two lines
    content = re.sub(
        r'\{ const TMP_EL = document\.getElementById\("metric-" \+ node\.id \+ "-uptime"\); if\(TMP_EL\) \{\s+TMP_EL\.innerText = m\.uptime; \} \}\s*\{ const TMP_EL = document\.getElementById\("metric-" \+ node\.id \+ "-plates"\); if\(TMP_EL\) \{\s+TMP_EL\.innerText = m\.plates; \} \}',
        '// (removed stray offline lines)',
        content
    )
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed via regex")
