import aiohttp
import asyncio


"""Przygotować korutynę, która asynchronicznie pobiera i zwraca zawartość strony internetowej z podanego adresu URL
   przy użyciu biblioteki aiohttp."""


async def download_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


if __name__ == '__main__':
    print(asyncio.run(download_page('https://www.google.com')))