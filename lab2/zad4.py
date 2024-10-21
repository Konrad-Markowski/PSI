import asyncio
from datetime import datetime, timedelta
import aiohttp


"""Przygotować korutynę, która zwróci prognozę pogody dla najbliszej godziny dla miasta Zakopane. Wykorzystać w tym celu 
   API Open-Meteo oraz przykładowy adres żądania: 
   https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"""


async def getForecast(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            hourly_data = data.get("hourly")
            times = hourly_data.get("time")
            temperatures = hourly_data.get("temperature_2m")
            humidity = hourly_data.get("relative_humidity_2m")
            wind_speed = hourly_data.get("wind_speed_10m")

            current_date = datetime.now().replace(minute=0, second=0, microsecond=0)
            next_hour = current_date + timedelta(hours=1)
            next_hour_string = next_hour.strftime("%Y-%m-%dT%H:%M")
            if next_hour_string in times:
                index = times.index(next_hour_string)
                temperature = temperatures[index]
                humidity_level = humidity[index]
                wind = wind_speed[index]

                return (f"Prognoza pogody dla Zakopanego na godzinę {next_hour_string}:\n"
                        f"Temperatura: {temperature}°C\n"
                        f"Wilgotność względna: {humidity_level}%\n"
                        f"Prędkość wiatru: {wind} km/h")

if __name__ == '__main__':
    url = "https://api.open-meteo.com/v1/forecast?latitude=49.299&longitude=19.9489&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    print(asyncio.run(getForecast(url)))