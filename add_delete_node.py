# -*- coding: utf-8 -*-
with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

delete_endpoint = '''
@app.delete("/api/nodes/{node_id}", dependencies=[Depends(verify_credentials)])
def delete_node(node_id: int, db: Session = Depends(get_db)):
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={"message": "Node not found"})
    db.delete(node)
    db.commit()
    return {"success": True}
'''

if 'def delete_node' not in text:
    text = text.replace('@app.delete("/api/projects/{project_id}', delete_endpoint + '\n@app.delete("/api/projects/{project_id}')

with open('fastapi_app/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added backend delete endpoint')
