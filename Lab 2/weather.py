import requests
# pip install requests

LATITUDE = 40.7128
LONGITUDE = -74.0060

def get_current_temperature():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current=temperature_2m"
        "&temperature_unit=fahrenheit"
    )

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()

    temperature = data["current"]["temperature_2m"]

    return round(temperature)