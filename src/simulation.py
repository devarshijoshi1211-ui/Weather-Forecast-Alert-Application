import pandas as pd


def create_simulated_forecast():
    records = [
        {
            "datetime_utc": "2026-11-24 12:00:00",
            "temp": 27.0, "feels_like": 27.5, "temp_min": 26.0, "temp_max": 28.0,
            "humidity": 45, "pressure": 1015, "wind_speed": 3.0, "wind_deg": 180,
            "weather_condition": "Clear", "weather_description": "clear sky",
            "clouds": 5, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.05
        },
        {
            "datetime_utc": "2026-11-24 15:00:00",
            "temp": 38.5, "feels_like": 40.0, "temp_min": 37.0, "temp_max": 39.0,
            "humidity": 85, "pressure": 1008, "wind_speed": 18.0, "wind_deg": 220,
            "weather_condition": "Thunderstorm", "weather_description": "thunderstorm with heavy rain",
            "clouds": 100, "rain_3h_mm": 12.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.90
        },
        {
            "datetime_utc": "2026-11-24 18:00:00",
            "temp": 25.0, "feels_like": 25.0, "temp_min": 24.0, "temp_max": 26.0,
            "humidity": 65, "pressure": 1010, "wind_speed": 5.0, "wind_deg": 250,
            "weather_condition": "Rain", "weather_description": "moderate rain",
            "clouds": 90, "rain_3h_mm": 4.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.75
        },
        {
            "datetime_utc": "2026-11-24 21:00:00",
            "temp": 22.0, "feels_like": 22.0, "temp_min": 21.0, "temp_max": 23.0,
            "humidity": 55, "pressure": 1013, "wind_speed": 2.5, "wind_deg": 280,
            "weather_condition": "Clear", "weather_description": "clear sky",
            "clouds": 0, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.0
        },
        {
            "datetime_utc": "2026-11-25 00:00:00",
            "temp": 20.0, "feels_like": 20.0, "temp_min": 19.0, "temp_max": 21.0,
            "humidity": 30, "pressure": 1016, "wind_speed": 2.0, "wind_deg": 300,
            "weather_condition": "Clear", "weather_description": "clear sky",
            "clouds": 0, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.0
        },
        {
            "datetime_utc": "2026-11-25 03:00:00",
            "temp": 19.0, "feels_like": 19.0, "temp_min": 18.0, "temp_max": 20.0,
            "humidity": 25, "pressure": 1017, "wind_speed": 1.5, "wind_deg": 310,
            "weather_condition": "Clear", "weather_description": "clear sky",
            "clouds": 0, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.0
        },
        {
            "datetime_utc": "2026-11-25 06:00:00",
            "temp": 31.0, "feels_like": 32.0, "temp_min": 30.0, "temp_max": 32.0,
            "humidity": 35, "pressure": 1014, "wind_speed": 4.0, "wind_deg": 120,
            "weather_condition": "Clouds", "weather_description": "scattered clouds",
            "clouds": 35, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.10
        },
        {
            "datetime_utc": "2026-11-25 09:00:00",
            "temp": 34.0, "feels_like": 35.0, "temp_min": 33.0, "temp_max": 35.0,
            "humidity": 40, "pressure": 1012, "wind_speed": 6.0, "wind_deg": 140,
            "weather_condition": "Clouds", "weather_description": "broken clouds",
            "clouds": 65, "rain_3h_mm": 0.0, "snow_3h_mm": 0.0,
            "probability_of_precipitation": 0.15
        }
    ]
    return pd.DataFrame(records).rename(columns={"temp": "temperature"})


def create_simulated_current_weather():
    return {
        "city": "Offline Demo City",
        "temperature": 27.0, "feels_like": 27.5,
        "minimum_temperature": 26.0, "maximum_temperature": 28.0,
        "humidity": 45, "pressure": 1015,
        "wind_speed": 3.0, "wind_direction": 180,
        "weather_condition": "Clear", "weather_description": "clear sky",
        "cloudiness": 5, "rain_1h_mm": 0.0, "rain_3h_mm": 0.0,
        "visibility_m": 10000,
        "observation_time_utc": "2026-11-24T12:00:00+00:00"
    }


print("Offline simulation module loaded successfully!")
