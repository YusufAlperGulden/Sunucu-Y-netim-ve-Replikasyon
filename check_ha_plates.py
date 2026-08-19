with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

idx = ha.find("plates_count = 'Metrik Ayarlanmad?'")
if idx == -1:
    idx = ha.find("plates_count =")
print(ha[idx:idx+1500].encode('ascii', errors='replace').decode('ascii'))
