import asyncio
import random


async def fetch(delay) -> int:
    await asyncio.sleep(delay)
    return random.randint(1, 10)


async def main() -> None:
    results = await asyncio.gather(fetch(2), fetch(4), fetch(6))
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
