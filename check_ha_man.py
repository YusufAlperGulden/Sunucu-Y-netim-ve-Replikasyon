with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

print("ha_manager.py get_server_metrics:")
print(ha[:2500].encode('ascii', errors='replace').decode('ascii'))
