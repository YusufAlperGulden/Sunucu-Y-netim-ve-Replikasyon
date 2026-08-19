import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace document.getElementById('X').innerText = Y
# Wait, let's just do it explicitly for the ones causing issues.
lines_to_fix = [
    "document.getElementById('detail-proj-name').innerText",
    "document.getElementById('detail-proj-desc').innerText",
    "document.getElementById('cc-total-clusters').innerText",
    "document.getElementById('cc-total-nodes').innerText",
    "document.getElementById('tt-cluster-id').innerText",
    "document.getElementById('tt-cluster-name').innerText",
    "document.getElementById('tt-cluster-vendor').innerText",
    "document.getElementById('tt-cluster-message-text').innerText",
    "document.getElementById('ntt-hostname').innerText",
    "document.getElementById('ntt-port').innerText",
    "document.getElementById('ntt-role').innerText",
    "document.getElementById('ntt-type').innerText",
    "document.getElementById('ntt-cluster').innerText",
    "document.getElementById('cc-donut-center-text').innerText",
    "document.getElementById('nodes-donut-center-num').innerText",
]

for item in lines_to_fix:
    element_id = re.search(r"getElementById\('([^']+)'\)", item).group(1)
    
    # We'll use a regex to replace `document.getElementById('ID').innerText = VALUE;`
    # Note: VALUE might be anything up to a semicolon or newline
    pattern = rf"document\.getElementById\('{element_id}'\)\.innerText\s*=\s*(.+?);"
    def replacer(match):
        val = match.group(1)
        var_name = f"el_{element_id.replace('-', '_')}"
        return f"const {var_name} = document.getElementById('{element_id}'); if({var_name}) {var_name}.innerText = {val};"
    
    content = re.sub(pattern, replacer, content)

# Let's also do innerHTML for good measure on missing elements
lines_to_fix_html = [
    "document.getElementById('detail-nodes-list').innerHTML",
]
for item in lines_to_fix_html:
    element_id = re.search(r"getElementById\('([^']+)'\)", item).group(1)
    pattern = rf"document\.getElementById\('{element_id}'\)\.innerHTML\s*=\s*(.+?);"
    def replacer_html(match):
        val = match.group(1)
        var_name = f"el_{element_id.replace('-', '_')}"
        return f"const {var_name} = document.getElementById('{element_id}'); if({var_name}) {var_name}.innerHTML = {val};"
    content = re.sub(pattern, replacer_html, content)

# Fix donutText.innerText
content = re.sub(r"donutText\.innerText\s*=\s*(.+?);", r"if(donutText) donutText.innerText = \1;", content)

# Fix donutHoverText2
content = re.sub(r"document\.getElementById\('donut-hover-text-2'\)\.innerText\s*=\s*(.+?);", r"const el_donut_txt2 = document.getElementById('donut-hover-text-2'); if(el_donut_txt2) el_donut_txt2.innerText = \1;", content)


with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched innerText assignments")
