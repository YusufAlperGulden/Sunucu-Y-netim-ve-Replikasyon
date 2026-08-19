import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

debug_endpoint = """
@app.get("/api/debug-db")
def debug_db(db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        res = db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='database_nodes';"))
        columns = [row[0] for row in res.fetchall()]
        
        # Test project 2 query directly
        proj = db.query(Project).filter(Project.id == 2).first()
        node_count = len(proj.nodes) if proj else -1
        
        return {"columns": columns, "proj_2_nodes": node_count}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
"""

if "def debug_db" not in content:
    content += "\n" + debug_endpoint
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added debug endpoint")
