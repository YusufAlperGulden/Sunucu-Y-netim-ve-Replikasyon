with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

idx = ha.find('def get_server_metrics')
if idx == -1:
    idx = ha.find('async def get_server_metrics')
print(ha[idx:idx+3500].encode('ascii', errors='replace').decode('ascii'))
