# weather_data.py

import requests

def get_weather_factor(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,precipitation"

        response = requests.get(url)
        data = response.json()

        current = data["current"]
        precipitation = current.get("precipitation", 0)
        wind_speed = current.get("wind_speed_10m", 0)

        
        weather_factor = 1.0

        if precipitation > 1:  # rain
            weather_factor += 0.2
        if wind_speed > 30:  # high wind
            weather_factor += 0.2

        return weather_factor

    except Exception as e:
        print("Weather API Error:", e)
        return 1.0  # default normal condition
