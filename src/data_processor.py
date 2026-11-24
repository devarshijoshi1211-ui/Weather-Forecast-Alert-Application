# ============================================================
# WEATHER FORECAST & ALERT APPLICATION
# PHASE 5: WEATHER DATA PROCESSING
# FILE: src/data_processor.py
# ============================================================

import pandas as pd

def process_current_weather(data):
    if not isinstance(data, dict):
        raise ValueError("Current weather data must be a dictionary.")
    if "main" not in data or "weather" not in data:
        raise ValueError("Incomplete current weather response.")
    main = data["main"]
    wind = data.get("wind", {})
    weather = data.get("weather", [{}])[0]
    rain = data.get("rain", {})
    processed = {
        "city": data.get("name", "Unknown"),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "minimum_temperature": main.get("temp_min"),
        "maximum_temperature": main.get("temp_max"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "wind_speed": wind.get("speed", 0),
        "wind_direction": wind.get("deg"),
        "weather_condition": weather.get("main", "Unknown"),
        "weather_description": weather.get("description", "Unknown"),
        "cloudiness": data.get("clouds", {}).get("all", 0),
        "rain_1h_mm": rain.get("1h", 0),
        "rain_3h_mm": rain.get("3h", 0),
        "visibility_m": data.get("visibility"),
        "observation_time_utc": pd.to_datetime(data.get("dt"), unit="s", utc=True) if data.get("dt") else pd.NaT
    }
    return processed

def process_forecast(data):
    if not isinstance(data, dict):
        raise ValueError("Forecast data must be a dictionary.")
    forecast_items = data.get("list", [])
    if not forecast_items:
        raise ValueError("No forecast records available.")
    records = []
    for item in forecast_items:
        main = item.get("main", {})
        weather = item.get("weather", [{}])[0]
        wind = item.get("wind", {})
        rain = item.get("rain", {})
        clouds = item.get("clouds", {})
        record = {
            "datetime_utc": pd.to_datetime(item.get("dt"), unit="s", utc=True),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "minimum_temperature": main.get("temp_min"),
            "maximum_temperature": main.get("temp_max"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind_speed": wind.get("speed", 0),
            "wind_direction": wind.get("deg"),
            "weather_condition": weather.get("main", "Unknown"),
            "weather_description": weather.get("description", "Unknown"),
            "cloudiness": clouds.get("all", 0),
            "rain_3h_mm": rain.get("3h", 0),
            "snow_3h_mm": item.get("snow", {}).get("3h", 0),
            "probability_of_precipitation": item.get("pop", 0)
        }
        records.append(record)
    df = pd.DataFrame(records)
    df = df.sort_values("datetime_utc").reset_index(drop=True)
    return df

def calculate_weather_statistics(df):
    if df.empty:
        raise ValueError("Cannot analyze an empty forecast.")
    required = ["temperature", "humidity"]
    for column in required:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    statistics = {
        "total_forecast_records": len(df),
        "average_temperature": round(df["temperature"].mean(), 2),
        "maximum_temperature": round(df["temperature"].max(), 2),
        "minimum_temperature": round(df["temperature"].min(), 2),
        "average_humidity": round(df["humidity"].mean(), 2),
        "maximum_humidity": round(df["humidity"].max(), 2),
        "minimum_humidity": round(df["humidity"].min(), 2),
        "maximum_rainfall_3h_mm": round(df["rain_3h_mm"].max(), 2),
        "maximum_precipitation_probability": round(df["probability_of_precipitation"].max() * 100, 2)
    }
    return statistics

def get_rainfall_forecast(df):
    if "rain_3h_mm" not in df.columns:
        raise ValueError("Rainfall column is missing.")
    rainy_periods = df[df["rain_3h_mm"] > 0].copy()
    return rainy_periods.reset_index(drop=True)

def get_temperature_extremes(df):
    if df.empty:
        raise ValueError("Forecast dataset is empty.")
    hottest = df.loc[df["temperature"].idxmax()]
    coldest = df.loc[df["temperature"].idxmin()]
    return {
        "hottest": hottest.to_dict(),
        "coldest": coldest.to_dict()
    }

def save_weather_dataset(df, filepath):
    df.to_csv(filepath, index=False)
    return filepath
