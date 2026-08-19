import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all instances of document.getElementById(...).innerText = ...
def replacer(match):
    full_call = match.group(0)
    # Extract the id expression inside getElementById
    id_expr_match = re.search(r"getElementById\((.*?)\)", full_call)
    if not id_expr_match:
        return full_call
    id_expr = id_expr_match.group(1)
    
    # We want to replace `document.getElementById(id_expr).innerText = value;`
    # with `const el_tmp = document.getElementById(id_expr); if(el_tmp) el_tmp.innerText = value;`
    
    # But some might already be fixed, like `const el_... = document.getElementById(...)`
    # If the line already starts with `const el_`, we skip it.
    
    return full_call

lines = content.split('\n')
new_lines = []
for line in lines:
    if "document.getElementById(" in line and ".innerText =" in line and "const el_" not in line and "if(document.getElementById" not in line:
        # It's a raw assignment
        # Let's extract the part before the = and the part after
        parts = line.split('.innerText =')
        if len(parts) == 2:
            left = parts[0]
            right = parts[1]
            # Replace left with a temporary variable guard
            # Extract id expression
            m = re.search(r"document\.getElementById\((.*?)\)", left)
            if m:
                id_expr = m.group(1)
                # Ensure it's safe to just inline
                # We'll use a unique temp var name per line
                safe_left = left.replace(m.group(0), "TMP_EL")
                new_line = f"{{ const TMP_EL = document.getElementById({id_expr}); if(TMP_EL) {{ {safe_left}.innerText ={right} }} }}"
                line = new_line
    
    # Same for .innerHTML =
    if "document.getElementById(" in line and ".innerHTML =" in line and "const el_" not in line and "if(document.getElementById" not in line and "if (" not in line and "if(" not in line:
        parts = line.split('.innerHTML =')
        if len(parts) == 2:
            left = parts[0]
            right = parts[1]
            m = re.search(r"document\.getElementById\((.*?)\)", left)
            if m:
                id_expr = m.group(1)
                safe_left = left.replace(m.group(0), "TMP_EL")
                new_line = f"{{ const TMP_EL = document.getElementById({id_expr}); if(TMP_EL) {{ {safe_left}.innerHTML ={right} }} }}"
                line = new_line

    new_lines.append(line)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
print("Patched all remaining innerText and innerHTML")
