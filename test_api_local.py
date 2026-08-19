import asyncio, aiohttp, json

async def test():
    async with aiohttp.ClientSession() as s:
        # Check what /api/projects returns
        async with s.get('http://localhost:8000/api/projects', headers={'Cookie': 'session=test'}) as r:
            print("Status:", r.status)
            if r.status == 200:
                data = await r.json()
                print(json.dumps(data, indent=2)[:2000])
asyncio.run(test())
