# -*- coding: utf-8 -*-
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

first_settings_start = content.find('<div id="settings-view" class="view-section" style="display: none;">')
first_settings_end = content.find('<!-- NODES VIEW -->', first_settings_start) - 10

second_settings_start = content.find('<div id="settings-view" class="view-section" style="display: none;">', first_settings_end)
second_settings_end = content.find('<!-- USERS VIEW -->', second_settings_start) - 10

if first_settings_start != -1 and second_settings_start != -1:
    print(f"First settings: {first_settings_start} to {first_settings_end}")
    print(f"Second settings: {second_settings_start} to {second_settings_end}")
