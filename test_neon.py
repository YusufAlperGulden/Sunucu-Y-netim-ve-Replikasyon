import os, asyncio
os.environ['VAULT_KEY'] = 'aT5XEmyjit99aWs2ej5QBCP84X--0HmFMXGDZNNX8j0='
os.environ['DATABASE_URL'] = 'sqlite:///./fastapi_app.db'
os.environ['ADMIN_USER'] = 'admin'
os.environ['ADMIN_PASS'] = 'admin'

import asyncpg, ssl

FRANKFURT = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test():
    for name, url in [("FRANKFURT", FRANKFURT), ("YEDEK", YEDEK)]:
        try:
            import time
            t = time.time()
            conn = await asyncpg.connect(url, timeout=8.0)
            ping = int((time.time()-t)*1000)
            row = await conn.fetchrow("SELECT pg_database_size(current_database()) as size, version()")
            await conn.close()
            print(f"{name}: OK - {ping}ms - {row['size']} bytes - {row['version'][:40]}")
        except Exception as e:
            print(f"{name}: FAILED - {type(e).__name__}: {e}")

asyncio.run(test())
