import asyncio


async def main() -> None:
    await asyncio.sleep(1)
    print("Hello")
    await asyncio.sleep(2)
    print("world")


if __name__ == "__main__":
    asyncio.run(main())