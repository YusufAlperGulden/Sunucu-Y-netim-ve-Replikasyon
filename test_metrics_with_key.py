import os
os.environ['VAULT_KEY'] = 'f_z9J8a7B6c5D4e3F2g1H0i9J8k7L6m5N4o3P2q1R0s='

import sys
sys.path.append('fastapi_app')

from vault import encrypt
from ha_manager import get_server_metrics
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
