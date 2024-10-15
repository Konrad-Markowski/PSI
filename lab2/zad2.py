import aiohttp
import asyncio


"""Przygotować korutynę, która asynchronicznie wyśle żądanie POST
   do REST API z treścią w formacie JSON i zwróci odpowiedź."""

async def post_json(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return await resp.json()


if __name__ == '__main__':
    sampleData = {'key': 'val'}
    print(asyncio.run(post_json('https://jsonplaceholder.typicode.com/posts', sampleData)))