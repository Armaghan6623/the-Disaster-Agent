import requests

def get_weather(latitude: float, longitude: float) -> dict:
    """Fetches current weather conditions for a given location."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,precipitation,wind_speed_10m",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return {
        "temperature_c": data["current"]["temperature_2m"],
        "precipitation_mm": data["current"]["precipitation"],
        "wind_speed_kmh": data["current"]["wind_speed_10m"],
    }