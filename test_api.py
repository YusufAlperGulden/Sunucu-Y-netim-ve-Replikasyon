import httpx
import asyncio

async def test():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://sunucu-yonetim-ve-replikasyon.onrender.com/api/projects/2", timeout=10)
            print("Status:", resp.status_code)
            print("Body:", resp.text)
    except Exception as e:
        print(e)

asyncio.run(test())
