import asyncio
from datetime import datetime, timedelta
import aiohttp

async def get_forecast(url: str, city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

def extract_forecast_details(forecast: dict, city: str) -> str:
    hourly_data = forecast.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    humidity = hourly_data.get("relative_humidity_2m", [])
    wind_speed = hourly_data.get("wind_speed_10m", [])

    current_date = datetime.now().replace(minute=0, second=0, microsecond=0)
    next_hour = current_date + timedelta(hours=1)
    next_hour_string = next_hour.strftime("%Y-%m-%dT%H:%M")

    if next_hour_string in times:
        index = times.index(next_hour_string)
        temperature = temperatures[index]
        humidity_level = humidity[index]
        wind = wind_speed[index]

        return (f"Prognoza pogody dla miasta '{city}' na godzinę {next_hour_string}:\n"
                f"Temperatura: {temperature}°C\n"
                f"Wilgotność względna: {humidity_level}%\n"
                f"Prędkość wiatru: {wind} km/h")
    else:
        return f"Brak danych pogodowych dla miasta '{city}' na godzinę {next_hour_string}."

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
    tasks = [(city, get_forecast(url, city)) for city, url in cities.items()]

    forecasts = await asyncio.gather(*(task[1] for task in tasks))

    filtered_forecasts = {}
    for (city, _), forecast in zip(tasks, forecasts):
        if filter_forecast(forecast, filter_mask):
            forecast_details = extract_forecast_details(forecast, city)
            filtered_forecasts[city] = forecast_details

    return filtered_forecasts

async def main() -> None:
    cities = {
        "Porlamar": "https://api.open-meteo.com/v1/forecast?latitude=10.957&longitude=-63.869&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        "Moroni": "https://api.open-meteo.com/v1/forecast?latitude=-11.702&longitude=43.255&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        "Helsinki": "https://api.open-meteo.com/v1/forecast?latitude=60.1699&longitude=24.9384&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    filter_mask = {
        "wind_speed_10m": "<20",
    }

    filtered_forecasts = await get_filtered_forecasts(cities, filter_mask)
    for city, forecast in filtered_forecasts.items():
        print(f"\n{forecast}")

if __name__ == "__main__":
    asyncio.run(main())
