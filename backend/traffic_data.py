from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="qwertyxzy123tanishqbhovare@gmail.com")
    location = geolocator.geocode(city_name + ", India")
    if location:
        return location.latitude, location.longitude
    else:
        return None
    

def get_traffic_data(city1, city2):
    coords_1 = get_coordinates(city1)
    coords_2 = get_coordinates(city2)

    if coords_1 and coords_2:
        distance_km = geodesic(coords_1, coords_2).kilometers
        travel_time_sec = (distance_km/80)*3600
        traffic_factor = travel_time_sec / (distance_km / 50 * 3600)  # assuming 50km/h as base speed
        return travel_time_sec, round(distance_km, 2), traffic_factor
        
    else:
        return "Unable to find coordinates for one or both cities."
    
