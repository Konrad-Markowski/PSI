import asyncio


async def krojenie() -> None:
    await asyncio.sleep(2)
    print("Pokrojone")


async def gotowanie() -> None:
    await asyncio.sleep(4)
    print("Pokrojone")