with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

idx = ha.find('if slots:')
print(ha[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
