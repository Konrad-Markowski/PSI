import asyncio


async def krojenie() -> None:
    print("Kroję...")
    await asyncio.sleep(2)
    print("Pokrojone")


async def gotowanie() -> None:
    print("Gotuję...")
    await asyncio.sleep(4)
    print("Ugotowane")


async def smazenie() -> None:
    print("Smażę...")
    await asyncio.sleep(3)
    print("Usmażone")

async def main() -> None:
    await asyncio.gather(krojenie(), gotowanie(), smazenie())


if __name__ == "__main__":
    asyncio.run(main())
