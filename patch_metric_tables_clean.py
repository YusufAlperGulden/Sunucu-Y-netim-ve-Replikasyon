with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

idx = ha.find('if metric_table:')
idx_start = ha.rfind('plates_count =', 0, idx)
idx_end = ha.find('# Fetch OS metrics', idx)

new_code = """plates_count = 'Metrik Ayarlanmadı'
            if metric_table:
                try:
                    count_row = await conn.fetchrow(f'SELECT count(*) as count FROM "{metric_table}"')
                    if count_row:
                        cnt = count_row['count']
                        if metric_table == 'vehicles':
                            plates_count = f"{cnt} Araç (vehicles)"
                        elif metric_table == 'emails':
                            plates_count = f"{cnt} E-posta (emails)"
                        else:
                            plates_count = f"{cnt} Kayıt ({metric_table})"
                except Exception:
                    plates_count = f"Tablo Bulunamadı ({metric_table})"
            
            """

if idx_start != -1 and idx_end != -1:
    ha = ha[:idx_start] + new_code + ha[idx_end:]
    with open('fastapi_app/ha_manager.py', 'w', encoding='utf-8') as f:
        f.write(ha)
    print("Patched ha_manager.py with dynamic table labels")

with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    main_py = f.read()

idx_ls = main_py.find('projects = db.query(Project).all()')
idx_ls_end = main_py.find('db.commit()', idx_ls + 500)

new_ls_sync = """projects = db.query(Project).all()
            for proj in projects:
                p_name = (proj.name or '').lower()
                if 'email' in p_name or 'e-mail' in p_name:
                    proj.metric_table = 'emails'
                elif 'plaka' in p_name or 'araç' in p_name:
                    proj.metric_table = 'vehicles'
                    
                nodes = proj.nodes
                if len(nodes) >= 2:
                    primary_nodes = [n for n in nodes if n.role and n.role.lower() == 'primary']
                    standby_nodes = [n for n in nodes if n.role and n.role.lower() == 'standby']
                    
                    FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
                    YEDEK_URL = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
                    
                    for node in primary_nodes:
                        current = decrypt(node.encrypted_url) if node.encrypted_url else None
                        if current != FRANKFURT_URL:
                            node.encrypted_url = encrypt(FRANKFURT_URL)
                            print(f"Updated primary node {node.id} URL to Frankfurt (Neon)")
                    
                    for node in standby_nodes:
                        current = decrypt(node.encrypted_url) if node.encrypted_url else None
                        if current != YEDEK_URL:
                            node.encrypted_url = encrypt(YEDEK_URL)
                            print(f"Updated standby node {node.id} URL to Yedek (Neon)")
                            
            db.commit()"""

if idx_ls != -1 and idx_ls_end != -1:
    main_py = main_py[:idx_ls] + new_ls_sync + main_py[idx_ls_end + len('db.commit()'):]
    with open('fastapi_app/main.py', 'w', encoding='utf-8') as f:
        f.write(main_py)
    print("Patched main.py lifespan")
