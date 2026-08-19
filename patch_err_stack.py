import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'if (errDiv) errDiv.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.toString())}</div>`;',
    'if (errDiv) errDiv.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.stack || error.toString())}</div>`;'
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated error logging to include stack trace")
