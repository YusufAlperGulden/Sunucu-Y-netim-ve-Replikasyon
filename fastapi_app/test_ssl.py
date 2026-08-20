# Quick test: can we connect to Neon with SSL?
import asyncio
import asyncpg
import ssl

async def test():
    # Test with a generic Neon-style URL format
    # Neon requires sslmode=require
    try:
        ctx = ssl.create_default_context()
        conn = await asyncpg.connect("postgresql://neondb_owner:test@ep-test.us-east-2.aws.neon.tech/neondb?sslmode=require", timeout=3.0, ssl=ctx)
        await conn.close()
        print("SSL connect worked")
    except Exception as e:
        print(f"SSL test error: {e}")

asyncio.run(test())
