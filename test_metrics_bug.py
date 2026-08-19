from fastapi_app.vault import encrypt
from fastapi_app.ha_manager import get_server_metrics
import asyncio

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

node = {
    'id': 1,
    'name': 'Ana Sunucu (Master)',
    'role': 'Primary',
    'encrypted_url': encrypt(FRANKFURT_URL),
    'metric_table': 'vehicles'
}

res = asyncio.run(get_server_metrics(node, 1))
print("Result:", res)
