import os

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

first_settings_start = content.find('<div id="settings-view" class="view-section" style="display: none;">')
first_settings_end = content.find('<!-- NODES VIEW -->', first_settings_start) - 10

second_settings_start = content.find('<div id="settings-view" class="view-section" style="display: none;">', first_settings_end)
second_settings_end = content.find('<!-- USERS VIEW -->', second_settings_start) - 10

with open('unified.part1', 'r', encoding='utf-8') as f:
    p1 = f.read()
with open('unified.part2', 'r', encoding='utf-8') as f:
    p2 = f.read()
with open('unified.part3', 'r', encoding='utf-8') as f:
    p3 = f.read()
with open('unified.part4', 'r', encoding='utf-8') as f:
    p4 = f.read()

unified_settings = p1 + p2 + p3 + p4

new_content = content[:first_settings_start] + unified_settings + content[first_settings_end:second_settings_start] + content[second_settings_end:]

# Now also add the Home icon next to Home
new_content = new_content.replace('<h1>Home</h1>', '<h1 style="display: flex; align-items: center; gap: 12px;"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg> Home</h1>')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Settings merged and Home icon added")
