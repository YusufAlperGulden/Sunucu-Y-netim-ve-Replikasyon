import asyncio, asyncpg, time

FRANKFURT = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test():
    t = time.time()
    conn = await asyncpg.connect(FRANKFURT, timeout=8.0)
    ping = int((time.time()-t)*1000)
    row = await conn.fetchrow("SELECT pg_database_size(current_database()) as size, version()")
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    await conn.close()
    print(f"FRANKFURT: OK - {ping}ms - {row['size']//1024} kB")
    print(f"Tables: {[r['table_name'] for r in tables]}")

asyncio.run(test())
