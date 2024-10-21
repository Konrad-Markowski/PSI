import asyncio
from datetime import datetime, timedelta
import aiohttp


"""Przygotować korutynę, która asynchronicznie pobierze prognozę pogody z API Open-Meteo dla kilku wybranych miast, 
   a następnie zwróci prognozy tylko dla tych miast, dla których prognoza spełnia warunki przekazane w słowniku będącym maską filtrowania. 
   Przykładowo, maska filtrowania zawierająca klucz wind_speed_10m o wartości < 20 pozostawi tylko te miasta, 
   które w prognozie pogody dla nadchodzących godzin będą miały przypisaną prędkośc wiatru o wartości < 20 km/h."""


async def get_forecast(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


def filter_forecast(forecast: dict, filter_mask: dict) -> bool:
    hourly_data = forecast.get("hourly")
    if not hourly_data:
        return False

    current_date = datetime.now().replace(minute=0, second=0, microsecond=0)
    next_hour = current_date + timedelta(hours=1)
    next_hour_string = next_hour.strftime("%Y-%m-%dT%H:%M")

    if next_hour_string in hourly_data["time"]:
        index = hourly_data["time"].index(next_hour_string)
        for key, condition in filter_mask.items():
            value = hourly_data.get(key, [None])[index]
            if value is None:
                return False

            operator, threshold = condition[0], float(condition[1:])
            if operator == "<" and not (value < threshold):
                return False
            elif operator == ">" and not (value > threshold):
                return False
            elif operator == "<=" and not (value <= threshold):
                return False
            elif operator == ">=" and not (value >= threshold):
                return False
            elif operator == "==" and not (value == threshold):
                return False
        return True

    return False


async def get_filtered_forecasts(cities: dict, filter_mask: dict) -> dict:
    tasks = []
    for city, url in cities.items():
        tasks.append((city, get_forecast(url)))

    forecasts = await asyncio.gather(*(task[1] for task in tasks))

    filtered_forecasts = {}
    for (city, _), forecast in zip(tasks, forecasts):
        if filter_forecast(forecast, filter_mask):
            filtered_forecasts[city] = forecast

    return filtered_forecasts


if __name__ == "__main__":
    cities = {
        "Porlamar": "https://api.open-meteo.com/v1/forecast?latitude=10.957&longitude=-63.869&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        "Moroni": "https://api.open-meteo.com/v1/forecast?latitude=-11.702&longitude=43.255&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        "Helsinki": "https://api.open-meteo.com/v1/forecast?latitude=60.1699&longitude=24.9384&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    filter_mask = {
        "wind_speed_10m": "<20",
    }

    filtered_forecasts = asyncio.run(get_filtered_forecasts(cities, filter_mask))
    for city, forecast in filtered_forecasts.items():
        print(f"{city}: Prognoza spełnia warunki filtrowania.")
