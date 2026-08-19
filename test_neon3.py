import asyncio, asyncpg

YEDEK = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test():
    import time
    conn = await asyncpg.connect(YEDEK, timeout=8.0)
    
    # Get tables list
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    print("Tables:", [r['table_name'] for r in tables])
    
    # Get pg_stat metrics
    row = await conn.fetchrow("""
        SELECT pg_database_size(current_database()) as db_size,
               (SELECT count(*) FROM pg_stat_activity) as active_conn,
               (SELECT setting::int FROM pg_settings WHERE name='max_connections') as max_conn
    """)
    print(f"DB Size: {row['db_size']//1024} kB, Connections: {row['active_conn']}/{row['max_conn']}")
    
    await conn.close()

asyncio.run(test())
