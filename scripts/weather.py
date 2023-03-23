from dotenv import load_dotenv
import os
import requests
from endpoint_data import Endpoint
import json

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_BASE_URL = os.getenv('WEATHER_BASE_URL')
WEATHER_POLLUTION_API = os.getenv('WEATHER_POLLUTION_API')
WEATHER_GEOCODING_API = os.getenv('WEATHER_GEOCODING_API')

def get_weather(city=None):
    if city == None:
        endpoint = Endpoint()
        lat = endpoint.lat
        lon = endpoint.lon
    else:
        geo_location = _get_location_from_city(city=city)
        lat = geo_location[0]
        lon = geo_location[1]

    params = {
        "lat": lat, 
        "lon": lon, 
        "appid": WEATHER_API_KEY, 
        }
    current_weather_response = requests.get(WEATHER_BASE_URL, params=params)
    pollution_response = requests.get(WEATHER_POLLUTION_API, params=params)

def _get_location_from_city(city):
    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }
    req = requests.get(WEATHER_GEOCODING_API, params=params)
    req_json = req.json()
    print(f"Pronađeno {req.json()}")
    return [req_json[0]["lat"], req_json[0]["lon"]] # we trust first will be correct; limit=1
