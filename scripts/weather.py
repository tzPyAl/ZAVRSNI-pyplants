from dotenv import load_dotenv
import os
import requests
from .endpoint_data import Endpoint
import json

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_BASE_URL = os.getenv('WEATHER_BASE_URL')
WEATHER_POLLUTION_API = os.getenv('WEATHER_POLLUTION_API')
WEATHER_GEOCODING_API = os.getenv('WEATHER_GEOCODING_API')

def get_weather(lat, lon):
    params = {
        "lat": lat, 
        "lon": lon, 
        "units": "metric",
        "appid": WEATHER_API_KEY, 
        }
    current_weather_response = requests.get(WEATHER_BASE_URL, params=params).json()
    pollution_response = requests.get(WEATHER_POLLUTION_API, params=params).json()
    return current_weather_response, pollution_response

def _get_location_from_city(city):
    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }
    req = requests.get(WEATHER_GEOCODING_API, params=params)
    req_json = req.json()
    if req_json:
        return [req_json[0]["name"], req_json[0]["country"], req_json[0]["lat"], req_json[0]["lon"]] # we trust first 
    else:
        return False
