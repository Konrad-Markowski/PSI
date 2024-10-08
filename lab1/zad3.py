import asyncio


async def fun1() -> None:
    await asyncio.sleep(3)
    print("Funkcja 1")


async def fun2() -> None:
    await asyncio.sleep(1)
    print("Funkcja 2")


async def main() -> None:
    results = await asyncio.gather(fun1(), fun2())


if __name__ == "__main__":
    asyncio.run(main())
