import asyncio


async def run():
    while True:
        print("running!")
        await asyncio.sleep(60.0)
