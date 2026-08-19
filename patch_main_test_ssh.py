import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

api_test_ssh = """
@app.post("/api/nodes/{node_id}/test-ssh", dependencies=[Depends(verify_credentials)])
def test_ssh_connection(node_id: int, db: Session = Depends(get_db)):
    from models import DatabaseNode
    from vault import decrypt
    from ssh_worker import SSHManager
    
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={"message": "Node not found"})
        
    if not node.ssh_host:
        return JSONResponse(status_code=400, content={"message": "SSH Host is not configured for this node."})
        
    credential = decrypt(node.encrypted_ssh_credential) if node.encrypted_ssh_credential else ""
    
    try:
        with SSHManager(node.ssh_host, node.ssh_port, node.ssh_username, credential) as ssh:
            stdout, stderr, code = ssh.execute_command("whoami")
            if code == 0:
                return {"success": True, "message": f"Successfully connected to SSH as {stdout.strip()}"}
            else:
                return {"success": False, "message": f"Connected, but command failed: {stderr}"}
    except Exception as e:
        return {"success": False, "message": f"SSH Connection failed: {str(e)}"}
"""

if "def test_ssh_connection" not in content:
    content += "\n" + api_test_ssh
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added SSH test endpoint")
else:
    print("Already added")
