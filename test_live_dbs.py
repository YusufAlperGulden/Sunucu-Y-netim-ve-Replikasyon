import asyncio, asyncpg, time

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
LONDRA_URL = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test_db(name, url):
    print(f"Testing {name}...")
    try:
        t0 = time.time()
        conn = await asyncpg.connect(url, timeout=10.0)
        t1 = time.time()
        ver = await conn.fetchval("SELECT version()")
        size = await conn.fetchval("SELECT pg_database_size(current_database())")
        count = await conn.fetchval("SELECT count(*) FROM vehicles") if await conn.fetchval("SELECT 1 FROM information_schema.tables WHERE table_name='vehicles'") else 0
        await conn.close()
        print(f"SUCCESS {name}: Ping={int((t1-t0)*1000)}ms, Ver={ver[:30]}, Size={size//1024}kB, Vehicles={count}")
    except Exception as e:
        print(f"FAILED {name}: {type(e).__name__} - {e}")

async def main():
    await test_db("Frankfurt", FRANKFURT_URL)
    await test_db("Londra", LONDRA_URL)

asyncio.run(main())
