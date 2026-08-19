import asyncio, asyncpg

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def check_tables():
    conn = await asyncpg.connect(FRANKFURT_URL)
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    print("Tables in Frankfurt Neon DB:")
    for t in tables:
        count = await conn.fetchval(f"SELECT count(*) FROM \"{t['table_name']}\"")
        print(f" - {t['table_name']} (row count: {count})")
    await conn.close()

asyncio.run(check_tables())
