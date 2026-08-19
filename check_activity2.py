content = open('fastapi_app/templates/index.html', encoding='utf-8').read()

# Find start and end of activity-view section
start_idx = content.find('<section id="activity-view"')
end_idx = content.find('<!-- OPERATIONAL REPORTS VIEW -->')
print(f"Start: {start_idx}, End: {end_idx}")
print(repr(content[end_idx-30:end_idx+10]))
