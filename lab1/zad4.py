import asyncio


async def timer() -> None:
    for i in range(1,6):
        print(i)
        await asyncio.sleep(1)
        i = i+1

if __name__ == "__main__":
    asyncio.run(timer())