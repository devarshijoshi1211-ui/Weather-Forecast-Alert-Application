# ============================================================
# PHASE 4: WEATHER API INTEGRATION
# FILE: src/weather_api.py
# ============================================================

from pathlib import Path
import requests
import os
from dotenv import load_dotenv

PROJECT_PATH = Path("/content/drive/MyDrive/Weather-Forecast-Alert-Application")
load_dotenv(PROJECT_PATH / ".env", override=True)

class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass

class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise WeatherAPIError("API key missing. Check your .env file.")
        self.session = requests.Session()
        self.timeout = 20

    def _make_request(self, endpoint, params):
        params["appid"] = self.api_key
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.timeout)
            if response.status_code == 401:
                raise WeatherAPIError("Unauthorized API key. Check the key or wait for activation.")
            if response.status_code == 404:
                raise WeatherAPIError("Requested weather resource not found.")
            if response.status_code == 429:
                raise WeatherAPIError("API request limit exceeded. Try later.")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Request timed out. Check your connection.")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Unable to connect to weather service.")
        except requests.exceptions.HTTPError:
            raise WeatherAPIError(f"Weather API returned HTTP {response.status_code}.")
        except ValueError:
            raise WeatherAPIError("Invalid JSON received from weather service.")

    def get_coordinates(self, city, country_code="IN"):
        if not city or not city.strip():
            raise WeatherAPIError("City name cannot be empty.")
        endpoint = "/geo/1.0/direct"
        data = self._make_request(endpoint, {"q": f"{city.strip()},{country_code}", "limit": 1})
        if not data:
            raise WeatherAPIError(f"City not found: {city}")
        location = data[0]
        return {
            "name": location.get("name", city),
            "state": location.get("state", ""),
            "country": location.get("country", country_code),
            "latitude": location["lat"],
            "longitude": location["lon"]
        }

    def get_current_weather(self, latitude, longitude):
        endpoint = "/data/2.5/weather"
        return self._make_request(endpoint, {"lat": latitude, "lon": longitude, "units": "metric"})

    def get_forecast(self, latitude, longitude):
        endpoint = "/data/2.5/forecast"
        return self._make_request(endpoint, {"lat": latitude, "lon": longitude, "units": "metric"})

    def close(self):
        self.session.close()
