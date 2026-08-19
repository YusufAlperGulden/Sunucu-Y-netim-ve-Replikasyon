import os, asyncio, asyncpg

# Use the correct Frankfurt URL from arac-plaka
FRANKFURT_OLD = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test():
    import time
    for name, url in [("FRANKFURT", FRANKFURT_OLD), ("YEDEK", YEDEK)]:
        try:
            t = time.time()
            conn = await asyncpg.connect(url, timeout=8.0)
            ping = int((time.time()-t)*1000)
            row = await conn.fetchrow("SELECT pg_database_size(current_database()) as size, version()")
            
            # Check tables
            tables = await conn.fetch("SELECT schemaname, tablename, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 5")
            await conn.close()
            print(f"{name}: OK - {ping}ms - size={row['size']//1024}kB")
            for t_row in tables:
                print(f"  Table: {t_row['tablename']} ({t_row['n_live_tup']} rows)")
        except Exception as e:
            print(f"{name}: FAILED - {type(e).__name__}: {e}")

asyncio.run(test())
