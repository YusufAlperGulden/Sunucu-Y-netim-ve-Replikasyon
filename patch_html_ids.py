import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<table style="width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 40px;">', '<table id="reports-table-element" style="width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 40px; display: none;">')
content = content.replace('<div style="text-align: center; color: #6b7280; font-size: 14px; padding: 20px;">\n                      <svg width="48"', '<div id="empty-reports-state" style="text-align: center; color: #6b7280; font-size: 14px; padding: 20px;">\n                      <svg width="48"')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added IDs to empty state")

