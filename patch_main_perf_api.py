import re

# 1. Add /api/projects/{project_id}/performance endpoint in main.py
with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    main_py = f.read()

perf_endpoint_code = """
@app.get('/api/projects/{project_id}/performance')
async def get_project_performance(project_id: int, db: Session = Depends(get_db)):
    from vault import decrypt
    import asyncpg
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
        
    primary_node = next((n for n in proj.nodes if n.role and n.role.lower() == 'primary'), None)
    standby_node = next((n for n in proj.nodes if n.role and n.role.lower() == 'standby'), None)
    
    data = {
        'variables': [],
        'queries': [],
        'schema': [],
        'deadlocks': 0,
        'nodes': [{'id': n.id, 'name': n.name, 'role': n.role} for n in proj.nodes]
    }
    
    target_node = primary_node or (proj.nodes[0] if proj.nodes else None)
    if target_node and target_node.encrypted_url:
        db_url = decrypt(target_node.encrypted_url)
        if db_url:
            try:
                conn = await asyncpg.connect(db_url, timeout=10)
                
                # Fetch settings variables
                vars_rows = await conn.fetch("SELECT name, setting, COALESCE(unit, '') as unit, short_desc FROM pg_settings ORDER BY name LIMIT 100")
                data['variables'] = [{
                    'name': r['name'],
                    'setting': r['setting'],
                    'unit': r['unit'],
                    'desc': r['short_desc']
                } for r in vars_rows]
                
                # Fetch active queries
                query_rows = await conn.fetch("SELECT pid, usename, COALESCE(client_addr::text, 'local') as client, state, query, COALESCE(age(clock_timestamp(), query_start)::text, '0s') as duration FROM pg_stat_activity WHERE state != 'idle' AND query NOT LIKE '%pg_stat_activity%' LIMIT 20")
                data['queries'] = [{
                    'pid': r['pid'],
                    'user': r['usename'],
                    'client': r['client'],
                    'state': r['state'],
                    'query': r['query'],
                    'duration': r['duration']
                } for r in query_rows]
                
                # Fetch schema tables
                schema_rows = await conn.fetch("SELECT table_name, (SELECT count(*) FROM information_schema.columns WHERE table_name = t.table_name) as col_count FROM information_schema.tables t WHERE table_schema='public' ORDER BY table_name")
                for r in schema_rows:
                    t_name = r['table_name']
                    try:
                        row_count = await conn.fetchval(f'SELECT count(*) FROM "{t_name}"')
                    except Exception:
                        row_count = 0
                    data['schema'].append({
                        'table_name': t_name,
                        'col_count': r['col_count'],
                        'row_count': row_count
                    })
                    
                # Fetch deadlocks count
                deadlocks_val = await conn.fetchval("SELECT deadlocks FROM pg_stat_database WHERE datname=current_database()")
                data['deadlocks'] = deadlocks_val or 0
                
                await conn.close()
            except Exception as e:
                print(f"Performance API DB error: {e}")
                
    return data
"""

if '/api/projects/{project_id}/performance' not in main_py:
    idx = main_py.find('@app.get("/api/projects/{project_id}/metrics")')
    if idx == -1:
        idx = main_py.find("@app.get('/api/projects/{project_id}/metrics')")
    main_py = main_py[:idx] + perf_endpoint_code + "\n\n" + main_py[idx:]
    with open('fastapi_app/main.py', 'w', encoding='utf-8') as f:
        f.write(main_py)
    print("Added /api/projects/{project_id}/performance endpoint to main.py")

