import os
os.environ['VAULT_KEY'] = 'f_z9J8a7B6c5D4e3F2g1H0i9J8k7L6m5N4o3P2q1R0s='

import sys
sys.path.append('fastapi_app')

from vault import encrypt
from ha_manager import get_server_metrics
import asyncio

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
LONDRA_URL = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

node_p = {
    'id': 1,
    'name': 'Ana Sunucu (Master)',
    'role': 'Primary',
    'encrypted_url': encrypt(FRANKFURT_URL),
    'metric_table': 'vehicles'
}

node_s = {
    'id': 2,
    'name': 'Yedek Sunucu (Standby)',
    'role': 'Standby',
    'encrypted_url': encrypt(LONDRA_URL),
    'metric_table': 'vehicles'
}

async def run_both():
    rp = await get_server_metrics(node_p, 1)
    rs = await get_server_metrics(node_s, 1)
    print("PRIMARY METRICS:", rp)
    print("STANDBY METRICS:", rs)

asyncio.run(run_both())
