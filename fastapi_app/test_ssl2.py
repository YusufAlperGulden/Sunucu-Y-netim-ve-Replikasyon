# Test: does asyncpg.connect WITHOUT ssl work on a Neon URL that has sslmode=require in the querystring?
import asyncio
import asyncpg

async def test():
    url = "postgresql://neondb_owner:test@ep-test.us-east-2.aws.neon.tech/neondb?sslmode=require"
    try:
        # Without explicit ssl= parameter but with sslmode in URL
        conn = await asyncpg.connect(url, timeout=3.0)
        await conn.close()
        print("URL-embedded SSL worked")
    except Exception as e:
        print(f"No SSL param: {type(e).__name__}: {e}")

asyncio.run(test())
