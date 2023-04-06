import requests

class Endpoint:
    def __init__(self):
        if self._get_location_from_ip() == None:
            self.ip = "0.0.0.0"
            self.city = "Unknown"
            self.country = "Unknown"
            self.lon = "Unknown"
            self.lat = "Unknown"

    def _get_ip(self):
        try:
            _ip_api = requests.get('https://api64.ipify.org?format=json')
        except:
            print("No internet connection")
            return False
        else:
            if _ip_api.status_code == 200:
                self.ip = _ip_api.json()["ip"]
                return self.ip
            else:
                print("Error while fetching external IP address, st:", _ip_api.status_code)
                return False

    def _get_location_from_ip(self):
        if self._get_ip():
            _location_api = requests.get(f'https://ipapi.co/{self.ip}/json/')
            if _location_api.status_code == 200:
                self.city = _location_api.json()["city"]
                self.region = _location_api.json()["region"]
                self.country = _location_api.json()["country_name"]
                self.population = _location_api.json()["country_population"]
                self.lat = _location_api.json()["latitude"]
                self.lon = _location_api.json()["longitude"]
                return True
            