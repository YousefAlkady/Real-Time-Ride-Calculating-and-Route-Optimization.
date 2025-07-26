import os
import requests
import time
import math
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found! Please set it in .env file.")

def get_coordinates(place_name, api_key):
    """
    Fetch longitude and latitude for a given place using OpenRouteService.
    """
    url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={place_name}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    coords = data["features"][0]["geometry"]["coordinates"]
    return coords[0], coords[1]  # (lon, lat)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two coordinates (in km).
    Earth is spherical, so we use the Haversine formula instead of simple subtraction.
    """
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_routes(start, end, api_key):
    """
    Fetch possible driving routes between start and end coordinates.
    """
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start}&end={end}&alternatives=true"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    routes = []
    for feature in data.get("features", []):
        distance = feature["properties"]["segments"][0]["distance"]
        duration = feature["properties"]["segments"][0]["duration"]
        routes.append({"distance": distance, "duration": duration})
    return routes

def choose_best_route(routes):
    """
    Selects the best route based on cost, time, and revenue scoring.
    """
    fuel_price = 13
    meters_per_litre = 35000
    base_fare = 10
    price_per_km = 2
    price_per_minute = 0.5

    fuel_weight = 1
    time_weight = 0.5
    revenue_weight = 1

    best_score = float('inf')
    best_index = -1

    for i, route in enumerate(routes):
        distance = route["distance"]
        duration = route["duration"]
        time_minutes = duration / 60

        fuel_cost = (distance / meters_per_litre) * fuel_price
        revenue = base_fare + (time_minutes * price_per_minute) + ((distance / 1000) * price_per_km)
        score = (fuel_cost * fuel_weight) + (time_minutes * time_weight) - (revenue * revenue_weight)

        print(f"Route {i + 1}: {distance / 1000:.1f} km, {time_minutes:.1f} min, Fuel Cost: {fuel_cost:.2f}, Revenue: {revenue:.2f}, Score: {score:.2f}")
        
        if score < best_score:
            best_score = score
            best_index = i

    return routes[best_index]

def simulate_driver_movement(start_lat, start_lon, target_lat, target_lon):
    """
    Simulates a driver moving step by step towards the destination.
    """
    driver_lat, driver_lon = start_lat, start_lon
    while haversine_distance(driver_lat, driver_lon, target_lat, target_lon) > 0.05:  # 50 meters
        driver_lat += 0.0005
        driver_lon += 0.0005
        print(f"Driver at ({driver_lat:.5f}, {driver_lon:.5f}) - Distance to target: {haversine_distance(driver_lat, driver_lon, target_lat, target_lon):.2f} km")
        time.sleep(1)
    print("Driver reached the destination!")

if __name__ == "__main__":
    start_place = input("Enter start location: ")
    end_place = input("Enter end location: ")

    start_lon, start_lat = get_coordinates(start_place, API_KEY)
    end_lon, end_lat = get_coordinates(end_place, API_KEY)

    start_coords = f"{start_lon},{start_lat}"
    end_coords = f"{end_lon},{end_lat}"

    routes = get_routes(start_coords, end_coords, API_KEY)
    if not routes:
        print("API failed. Using fallback test routes.")
        routes = [{"distance": 60000, "duration": 4800}, {"distance": 80000, "duration": 3600}]

    best_route = choose_best_route(routes)
    print(f"Best Route Selected: {best_route}")
    simulate_driver_movement(start_lat, start_lon, end_lat, end_lon)
