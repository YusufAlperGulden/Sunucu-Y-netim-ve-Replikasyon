import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the click listener for sidebar categories and add code to clear the search input.
old_click_handler = """            // Load settings for this category
            loadSettings(item.dataset.category);"""

new_click_handler = """            // Clear search input if a category is manually clicked
            const searchInput = document.getElementById('settings-search-input');
            if (searchInput && searchInput.value) {
                searchInput.value = '';
            }
            
            // Load settings for this category
            loadSettings(item.dataset.category);"""

if "searchInput.value = '';" not in content:
    content = content.replace(old_click_handler, new_click_handler)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added search clear on category click")
else:
    print("Already added")
