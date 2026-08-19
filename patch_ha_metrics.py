import re

ha_path = 'fastapi_app/ha_manager.py'
with open(ha_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to change get_server_metrics signature
old_sig = "async def get_server_metrics(encrypted_url: str, project_id: int = None, role: str = None, metric_table: str = None) -> dict:"
new_sig = "async def get_server_metrics(node: dict, project_id: int = None) -> dict:"

if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("Found and replaced old_sig")

# Fix references to url inside get_server_metrics
old_url_decrypt = """    try:
        url = decrypt(encrypted_url)
        if not url:"""
new_url_decrypt = """    try:
        url = decrypt(node['encrypted_url'])
        role = node['role']
        metric_table = node.get('metric_table')
        if not url:"""
content = content.replace(old_url_decrypt, new_url_decrypt)

# Now, add SSH OS metrics fetching!
old_return = "                'tup_deleted': tup_deleted\n            }"
new_return = """                'tup_deleted': tup_deleted,
                'cpu_usage': os_metrics.get('cpu', 'N/A'),
                'ram_usage': os_metrics.get('ram', 'N/A')
            }"""
content = content.replace(old_return, new_return)

# Inject the OS fetching code before the return
os_fetch_code = """
            # Fetch OS metrics via SSH if available
            os_metrics = {'cpu': 'N/A', 'ram': 'N/A'}
            if node.get('ssh_host') and node.get('encrypted_ssh_credential'):
                import asyncio
                
                def fetch_os():
                    from ssh_worker import SSHManager
                    ssh_cred = decrypt(node['encrypted_ssh_credential'])
                    if not ssh_cred: return {}
                    try:
                        with SSHManager(node['ssh_host'], node.get('ssh_port', 22), node.get('ssh_username', 'root'), ssh_cred) as ssh:
                            # Basic Linux commands for CPU and RAM
                            cpu_out, _, _ = ssh.execute_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
                            ram_out, _, _ = ssh.execute_command("free -m | awk 'NR==2{printf \\"%.1f\\", $3*100/$2 }'")
                            
                            cpu = cpu_out.strip()
                            ram = ram_out.strip()
                            return {'cpu': f"{cpu}%" if cpu else 'N/A', 'ram': f"{ram}%" if ram else 'N/A'}
                    except Exception as e:
                        print("SSH Metric error:", e)
                        return {}
                
                try:
                    os_res = await asyncio.to_thread(fetch_os)
                    os_metrics.update(os_res)
                except:
                    pass
"""
# insert os_fetch_code right before the final return dict
content = content.replace("return {\n                'status': 'online',", os_fetch_code + "\n            return {\n                'status': 'online',")

with open(ha_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ha_manager.py")
