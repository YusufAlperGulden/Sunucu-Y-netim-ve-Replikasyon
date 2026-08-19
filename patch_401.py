import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix fetchProjects 401 handling so it doesn't print to screen
old_err_handling = """              if (!response.ok) {
                  const errText = await response.text();
                  const errDiv = document.getElementById('projects-container');
                  if (errDiv) errDiv.insertAdjacentHTML("afterbegin", `<div class="loading-state" style="color: var(--danger)">Error loading projects. Server returned ${response.status}: ${escapeHTML(errText)}</div>`);
                  return;
              }"""

new_err_handling = """              if (!response.ok) {
                  if (response.status === 401) return; // Handled by apiFetch
                  const errText = await response.text();
                  const errDiv = document.getElementById('projects-container');
                  if (errDiv) errDiv.insertAdjacentHTML("afterbegin", `<div class="loading-state" style="color: var(--danger)">Error loading projects. Server returned ${response.status}: ${escapeHTML(errText)}</div>`);
                  return;
              }"""

content = content.replace(old_err_handling, new_err_handling)

# Let's also remove any piled up errors at the start of fetchProjects
old_start = """    async function fetchProjects() {
        try {
            const response = await apiFetch('/api/projects');"""
            
new_start = """    async function fetchProjects() {
        try {
            // Clear any old error messages
            document.querySelectorAll('.loading-state').forEach(el => el.remove());
            const response = await apiFetch('/api/projects');"""

content = content.replace(old_start, new_start)


with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched fetchProjects 401 and error clearing")
