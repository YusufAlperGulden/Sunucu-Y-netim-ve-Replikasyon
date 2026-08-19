import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_load_logic = """            let filteredDefs = settingsDefs.filter(d => d.category === currentSettingsCategory);"""

new_load_logic = """            let searchQuery = '';
            const searchInput = document.getElementById('settings-search-input');
            if (searchInput) searchQuery = searchInput.value.toLowerCase().trim();

            let filteredDefs = [];
            if (searchQuery) {
                // Search across ALL categories
                filteredDefs = settingsDefs.filter(d => {
                    let valStr = String(data[d.key] || '').toLowerCase();
                    return d.key.toLowerCase().includes(searchQuery) ||
                           d.desc.toLowerCase().includes(searchQuery) ||
                           valStr.includes(searchQuery);
                });
            } else {
                // Filter by selected category
                filteredDefs = settingsDefs.filter(d => d.category === currentSettingsCategory);
            }"""

if "let searchQuery = '';" not in content:
    content = content.replace(old_load_logic, new_load_logic)

# We also need to add the event listener for the search input
event_listener_js = """
    // Add search listener for settings
    const settingsSearchInput = document.getElementById('settings-search-input');
    if (settingsSearchInput) {
        settingsSearchInput.addEventListener('input', () => {
            // Debounce or just load directly since data fetch is fast or we could cache it, 
            // but for simplicity we'll just call loadSettings
            // Actually it hits API every time. Let's debounce it slightly or just do it.
            if (window.settingsSearchTimeout) clearTimeout(window.settingsSearchTimeout);
            window.settingsSearchTimeout = setTimeout(() => {
                loadSettings();
            }, 300);
        });
    }
"""

if "settingsSearchInput.addEventListener" not in content:
    # insert it right before the click listeners to sidebar
    insert_marker = "// Add click listeners to sidebar categories"
    if insert_marker in content:
        content = content.replace(insert_marker, event_listener_js + "\n    " + insert_marker)
    else:
        # Fallback insert location
        content += "\n" + event_listener_js

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Implemented search filter logic")
