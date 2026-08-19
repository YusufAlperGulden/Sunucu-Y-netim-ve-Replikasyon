import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the hardcoded maria/percona msg logic
old_msg_logic = r'// BUT let\'s also hardcode some messages based on project name matching user screenshots.*?let msg = null;.*?if \(nameLower\.includes\(\'maria\'\)\) msg = .*?;.*?if \(nameLower\.includes\(\'percona mysql\'\)\) msg = .*?;'

new_msg_logic = """// Determine if there is a disabled node
                          let msg = null;
                          const cNodes = allNodes.filter(nd => nd.clusterId === proj.id && nd.status === 'Shut Down');
                          if (cNodes.length > 0) {
                              const n = cNodes[0];
                              const r = n.role ? (n.role.charAt(0).toUpperCase() + n.role.slice(1)) : 'None';
                              const port = r === 'ProxySQL' ? 6032 : (vendorType === 'postgres' ? 5432 : 3306);
                              msg = `${n.name}:${port} (${r}): Node is shutdown by user`;
                          }"""

js_content = re.sub(old_msg_logic, new_msg_logic, js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated message logic.")
