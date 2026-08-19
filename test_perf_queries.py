import asyncio, asyncpg, json

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

async def test_perf_queries():
    conn = await asyncpg.connect(FRANKFURT_URL)
    
    # 1. DB Variables (sample)
    vars_rows = await conn.fetch("SELECT name, setting, COALESCE(unit, '') as unit, short_desc FROM pg_settings WHERE name in ('autovacuum', 'checkpoint_timeout', 'max_connections', 'shared_buffers', 'work_mem', 'wal_level', 'hot_standby', 'temp_buffers', 'track_activities', 'deadlock_timeout') ORDER BY name")
    print("DB Variables sample:")
    for r in vars_rows:
        print(f" - {r['name']}: {r['setting']} {r['unit']} ({r['short_desc']})")
        
    # 2. Schema tables
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    print(f"\nTables count: {len(tables)}")
    
    # 3. Deadlocks count
    deadlocks = await conn.fetchval("SELECT deadlocks FROM pg_stat_database WHERE datname=current_database()")
    print(f"Deadlocks count in DB: {deadlocks}")
    
    await conn.close()

asyncio.run(test_perf_queries())
