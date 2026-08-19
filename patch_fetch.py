import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix fetchProjects 401 handling
pattern = r"if \(!response\.ok\) \{\s*const errText = await response\.text\(\);\s*projectsContainer\.innerHTML = `<div class=\"loading-state\".*?</div>`;\s*return;\s*\}"
def replacer(match):
    return """if (!response.ok) {
                  if (response.status === 401) return; // Handled by apiFetch
                  const errText = await response.text();
                  projectsContainer.insertAdjacentHTML('afterbegin', `<div class="loading-state" style="color: var(--danger)">Error loading projects. Server returned ${response.status}: ${escapeHTML(errText)}</div>`);
                  return;
              }"""

content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Add a guard for tbody.querySelectorAll('tr') in case tbody is still null for some reason
pattern_query = r"const rows = tbody\.querySelectorAll\('tr'\);"
content = content.replace(pattern_query, "const rows = tbody ? tbody.querySelectorAll('tr') : [];")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched fetchProjects properly")
