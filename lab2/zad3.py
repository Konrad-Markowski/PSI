import asyncio
import aiohttp


"""Przygotować program, który asynchronicznie pobiera treści z 5 
   różnych (dowolnych) stron internetowych w sposób współbieżny."""


async def download_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


