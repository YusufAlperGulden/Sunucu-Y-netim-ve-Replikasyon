with open('fastapi_app/ha_manager.py', 'r', encoding='utf-8') as f:
    ha = f.read()

# Refine formatting in get_server_metrics in ha_manager.py
import re

# Update xact formatting
ha = ha.replace("'xact': f'{commits} / {rollbacks}'", "'xact': f'{commits:,} ✓ / {rollbacks:,} ✗'")

# Update uptime formatting
ha = re.sub(
    r"uptime = str\(uptime_row\['uptime'\]\) if uptime_row else 'Unknown'",
    """raw_uptime = str(uptime_row['uptime']) if uptime_row else 'Unknown'
            uptime = raw_uptime.replace('days', 'gün').replace('day', 'gün')""",
    ha
)

with open('fastapi_app/ha_manager.py', 'w', encoding='utf-8') as f:
    f.write(ha)

print("Refined formatting in ha_manager.py")
