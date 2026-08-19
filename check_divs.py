import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def check_tags(content, tag_name):
    opens = len(re.findall(f'<{tag_name}', content))
    closes = len(re.findall(f'</{tag_name}>', content))
    return opens, closes

print("divs:", check_tags(content, 'div'))
print("sections:", check_tags(content, 'section'))
