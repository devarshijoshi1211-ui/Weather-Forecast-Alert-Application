# ============================================================
# WEATHER FORECAST & ALERT APPLICATION
# PHASE 6: FORECAST ANALYSIS ENGINE
# FILE: src/forecast_analyzer.py
# ============================================================

import pandas as pd


def prepare_local_forecast(df, timezone_offset_seconds=0):
    """Add local timestamps and dates using the city's UTC offset."""
    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    if "datetime_utc" not in df.columns:
        raise ValueError("datetime_utc column is missing.")

    result = df.copy()

    utc_times = pd.to_datetime(result["datetime_utc"], utc=True)

    result["datetime_local"] = (
        utc_times + pd.to_timedelta(timezone_offset_seconds, unit="s")
    ).dt.tz_localize(None)

    result["forecast_date"] = result["datetime_local"].dt.date
    result["forecast_hour"] = result["datetime_local"].dt.hour

    return result


def analyze_daily_forecast(df):
    """Calculate daily temperature, humidity, and rainfall summaries."""
    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    required = ["forecast_date", "temperature", "humidity"]
    for column in required:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")

    daily = df.groupby("forecast_date").agg(
        average_temperature=("temperature", "mean"),
        maximum_temperature=("temperature", "max"),
        minimum_temperature=("temperature", "min"),
        average_humidity=("humidity", "mean"),
        maximum_humidity=("humidity", "max"),
        minimum_humidity=("humidity", "min"),
        forecast_intervals=("temperature", "count")
    ).reset_index()

    if "rain_3h_mm" in df.columns:
        rainfall = df.groupby("forecast_date")["rain_3h_mm"].sum()
        daily["total_forecast_rainfall_mm"] = (
            daily["forecast_date"].map(rainfall)
        )

    if "probability_of_precipitation" in df.columns:
        precipitation = df.groupby("forecast_date")[
            "probability_of_precipitation"
        ].max() * 100
        daily["maximum_rain_probability_percent"] = (
            daily["forecast_date"].map(precipitation)
        )

    temperature_columns = [
        "average_temperature",
        "maximum_temperature",
        "minimum_temperature",
        "average_humidity",
        "maximum_humidity",
        "minimum_humidity"
    ]

    daily[temperature_columns] = daily[temperature_columns].round(2)

    return daily


def analyze_temperature_trend(df):
    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    ordered = df.sort_values("datetime_local")

    first_temperature = float(ordered.iloc[0]["temperature"])
    last_temperature = float(ordered.iloc[-1]["temperature"])
    change = round(last_temperature - first_temperature, 2)

    if change > 1:
        trend = "Rising"
    elif change < -1:
        trend = "Falling"
    else:
        trend = "Relatively Stable"
    return {
        "starting_temperature": round(first_temperature, 2),
        "ending_temperature": round(last_temperature, 2),
        "temperature_change": change,
        "trend": trend
    }


def analyze_humidity(df):
    """Summarize humidity levels and identify high-humidity intervals."""
    if df.empty or "humidity" not in df.columns:
        raise ValueError("Valid humidity forecast data is required.")

    return {
        "average_humidity": round(float(df["humidity"].mean()), 2),
        "maximum_humidity": int(df["humidity"].max()),
        "minimum_humidity": int(df["humidity"].min()),
        "high_humidity_intervals": int((df["humidity"] >= 80).sum()),
        "low_humidity_intervals": int((df["humidity"] <= 30).sum())
    }


def analyze_precipitation(df):
    """Analyze forecast rainfall and probability of precipitation."""
    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    rainfall = df.get(
        "rain_3h_mm", pd.Series(0, index=df.index)
    ).fillna(0)
    probability = df.get(
        "probability_of_precipitation", pd.Series(0, index=df.index)
    ).fillna(0)

    rainy_intervals = int((rainfall > 0).sum())
    likely_rain_intervals = int((probability >= 0.5).sum())

    return {
        "total_forecast_rainfall_mm": round(float(rainfall.sum()), 2),
        "maximum_rainfall_3h_mm": round(float(rainfall.max()), 2),
        "rainy_intervals": rainy_intervals,
        "maximum_rain_probability_percent": round(float(probability.max()) * 100, 2),
        "intervals_with_at_least_50_percent_rain_probability": likely_rain_intervals
    }


def summarize_weather_conditions(df):
    """Count forecast intervals by weather condition."""
    if df.empty or "weather_condition" not in df.columns:
        raise ValueError("Weather condition data is required.")

    return (
        df["weather_condition"]
        .fillna("Unknown")
        .value_counts()
        .to_dict()
    )


def generate_forecast_insights(
    daily_summary, temperature_trend, humidity_analysis,
    precipitation_analysis, condition_summary
):
    """Generate readable observations from forecast analysis."""
    insights = []

    hottest_day = daily_summary.loc[
        daily_summary["maximum_temperature"].idxmax()
    ]
    coolest_day = daily_summary.loc[
        daily_summary["minimum_temperature"].idxmin()
    ]

    insights.append(
        f"Hottest forecast day: {hottest_day['forecast_date']} "
        f"with a maximum temperature of {hottest_day['maximum_temperature']:.1f} °C."
    )

    insights.append(
        f"Coolest forecast day: {coolest_day['forecast_date']} "
        f"with a minimum temperature of {coolest_day['minimum_temperature']:.1f} °C."
    )

    insights.append(
        f"Overall temperature trend: {temperature_trend['trend']} "
        f"({temperature_trend['temperature_change']:+.1f} °C "
        f"from the first to the last forecast interval)."
    )

    insights.append(
        f"Average forecast humidity: {humidity_analysis['average_humidity']:.1f}%."
    )

    if precipitation_analysis["rainy_intervals"] > 0:
        insights.append(
            f"Rain is forecast in {precipitation_analysis['rainy_intervals']} intervals."
        )
    elif precipitation_analysis["intervals_with_at_least_50_percent_rain_probability"] > 0:
        insights.append(
            "No rainfall amount is currently recorded, but some intervals "
            "have at least a 50% probability of precipitation."
        )
    else:
        insights.append(
            "No rainfall is recorded and no interval reaches "
            "50% precipitation probability."
        )

    most_common_condition = max(
        condition_summary, key=condition_summary.get
    )
    insights.append(
        f"Most common forecast condition: {most_common_condition}."
    )

    return insights
