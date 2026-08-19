with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

idx = ha.find('async def get_server_metrics')
print(ha[idx:idx+4000].encode('ascii', errors='replace').decode('ascii'))
