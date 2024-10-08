import asyncio


async def main() -> None:
    await asyncio.sleep(2)
    print("Oczekiwanie zakończone")

if __name__ == "__main__":
    asyncio.run(main())