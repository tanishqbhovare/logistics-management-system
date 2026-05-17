# backend/route_prediction.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
MAPMYINDIA_API_KEY = os.getenv("MAPMYINDIA_API_KEY")

def get_route_data(lat1, lon1, lat2, lon2):
    """
    Fetches base distance (km) and time (min) from MapMyIndia Route Planner API.
    This gives you the ‘free‑flow’ estimate without traffic/weather adjustments.
    """
    url = (
        f"https://atlas.mapmyindia.com/api/routeplanner/v1/directions/json"
        f"?from={lat1},{lon1}&to={lat2},{lon2}&profile=driving"
    )
    headers = {
        "Authorization": f"bearer {MAPMYINDIA_API_KEY}"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("MapMyIndia routing error:", resp.text)
        return None, None

    data = resp.json()
    routes = data.get("routes")
    if not routes:
        return None, None

    summary = routes[0]["summary"]
    # distance in km, time in minutes
    distance_km = round(summary["distance"] / 1000, 2)
    base_time_min = round(summary["duration"] / 60, 2)
    return base_time_min, distance_km

def predict_travel_time(lat1, lon1, lat2, lon2, traffic_factor, weather_factor):
    """
    Combines base travel time with real-time traffic & weather factors
    to produce an adjusted ETA.
    """
    base_time, distance = get_route_data(lat1, lon1, lat2, lon2)
    if base_time is None or distance is None:
        return None, None

    # Adjust the base time
    adjusted_time = round(base_time * traffic_factor * weather_factor, 2)
    return adjusted_time, distance

# def predict_travel_time(traffic_factor, weather_factor):
#     """
#     Combines base travel time with real-time traffic & weather factors
#     to produce an adjusted ETA.
#     """
#     base_time, distance = get_route_data(lat1, lon1, lat2, lon2)
#     if base_time is None or distance is None:
#         return None, None

#     # Adjust the base time
#     adjusted_time = round(base_time * traffic_factor * weather_factor, 2)
#     return adjusted_time, distance

