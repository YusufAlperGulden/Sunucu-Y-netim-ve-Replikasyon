import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find the start of the syntax error
start_idx = content.find("</td>\n                <td style=\"padding: 16px 10px; color: #6b7280;\">")

if start_idx != -1:
    # Look for the end of the old renderBackups function
    # It ends with:
    #         `).join('');
    #     }
    # }
    end_pattern = "`).join('');\n    }\n}"
    end_idx = content.find(end_pattern, start_idx)
    if end_idx != -1:
        # Delete the broken chunk
        content = content[:start_idx] + content[end_idx + len(end_pattern):]
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed JS syntax error!")
    else:
        print("End pattern not found.")
else:
    print("Start index not found.")
