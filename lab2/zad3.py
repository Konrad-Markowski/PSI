import asyncio
import aiohttp


"""Przygotować program, który asynchronicznie pobiera treści z 5 
   różnych (dowolnych) stron internetowych w sposób współbieżny."""


async def download_page(urls: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(urls) as response:
            return await response.text()


async def download_all(urls: list) -> list:
    tasks = [download_page(url) for url in urls]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = [
        "http://www.google.com",
        "https://www.example.org",
        "https://stackoverflow.com/",
        "https://www.wikipedia.org"
    ]
    results = asyncio.run(download_all(urls))
    for i, zawartosc in enumerate(results):
        print(f"Zawartość strony: {urls[i]}")
        print(zawartosc[:2000])
        print("-------------------------------------------------------------------------------------")