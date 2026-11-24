
# ============================================================
# WEATHER FORECAST & ALERT APPLICATION
# PHASE 7: WEATHER ALERT SYSTEM
# FILE: src/alert_system.py
# ============================================================

import pandas as pd


DEFAULT_THRESHOLDS = {
    "high_temperature_c": 35.0,
    "high_humidity_percent": 80,
    "rain_probability": 0.60,
    "heavy_rain_3h_mm": 10.0,
    "high_wind_speed_ms": 15.0
}

SEVERE_CONDITIONS = {
    "tornado",
    "squall"
}

def validate_thresholds(thresholds):
    """Combine user thresholds with defaults and validate their values."""
    settings = DEFAULT_THRESHOLDS.copy()

    if thresholds:
        unknown = set(thresholds) - set(DEFAULT_THRESHOLDS)
        if unknown:
            raise ValueError(
                f"Unknown threshold settings: {sorted(unknown)}"
            )
        settings.update(thresholds)

    for key, value in settings.items():
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"Threshold '{key}' must be a non-negative number."
            )

    if settings["high_humidity_percent"] > 100:
        raise ValueError("Humidity threshold cannot exceed 100.")

    if settings["rain_probability"] > 1:
        raise ValueError(
            "Rain probability threshold must be between 0 and 1."
        )

    return settings


def create_alert(
    category, severity, forecast_time, message, measured_value=None
):
    """Create one consistently structured weather alert."""
    return {
        "category": category,
        "severity": severity,
        "forecast_time": forecast_time,
        "message": message,
        "measured_value": measured_value
    }


def generate_weather_alerts(df, thresholds=None):
    """Inspect forecast intervals and generate alerts.

    Rain probability is expected as a fraction from 0 to 1,
    matching the OpenWeatherMap forecast response.
    """
    if df.empty:
        raise ValueError("Cannot generate alerts from an empty forecast.")

    required = ["temperature", "humidity", "weather_condition"]
    for column in required:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")

    settings = validate_thresholds(thresholds)
    alerts = []

    for _, row in df.iterrows():
        forecast_time = row.get(
            "datetime_local", row.get("datetime_utc", "Unknown")
        )

        temperature = row.get("temperature")
        humidity = row.get("humidity")
        condition = str(row.get("weather_condition", "Unknown")).strip()
        normalized_condition = condition.lower()

        # High temperature alert
        if pd.notna(temperature) and temperature >= settings["high_temperature_c"]:
            alerts.append(create_alert(
                "High Temperature",
                "High",
                forecast_time,
                f"Temperature may reach {temperature:.1f} °C.",
                round(float(temperature), 2)
            ))

        # High humidity alert
        if pd.notna(humidity) and humidity >= settings["high_humidity_percent"]:
            alerts.append(create_alert(
                "High Humidity",
                "Moderate",
                forecast_time,
                f"Humidity may reach {humidity:.0f}%.",
                round(float(humidity), 2)
            ))

        # Rainfall alert
        rainfall = row.get("rain_3h_mm", 0)
        if pd.notna(rainfall) and rainfall > 0:
            severity = (
                "High" if rainfall >= settings["heavy_rain_3h_mm"]
                else "Moderate"
            )
            alerts.append(create_alert(
                "Rainfall",
                severity,
                forecast_time,
                f"Rainfall of {rainfall:.1f} mm is forecast in 3 hours.",
                round(float(rainfall), 2)
            ))

        # Probability of precipitation alert
        probability = row.get("probability_of_precipitation", 0)
        if pd.notna(probability) and probability >= settings["rain_probability"]:
            alerts.append(create_alert(
                "High Rain Probability",
                "Moderate",
                forecast_time,
                f"Probability of precipitation is {probability * 100:.0f}%.",
                round(float(probability) * 100, 2)
            ))

        # High wind alert
        wind_speed = row.get("wind_speed", 0)
        if pd.notna(wind_speed) and wind_speed >= settings["high_wind_speed_ms"]:
            alerts.append(create_alert(
                "High Wind",
                "High",
                forecast_time,
                f"Wind speed may reach {wind_speed:.1f} m/s.",
                round(float(wind_speed), 2)
            ))

        # Thunderstorm alert
        if normalized_condition == "thunderstorm":
            alerts.append(create_alert(
                "Thunderstorm",
                "High",
                forecast_time,
                "Thunderstorm conditions are forecast."
            ))

        # Severe weather alert
        if normalized_condition in SEVERE_CONDITIONS:
            alerts.append(create_alert(
                "Severe Weather",
                "Critical",
                forecast_time,
                f"Potentially severe weather condition: {condition}."
            ))

    alert_df = pd.DataFrame(
        alerts,
        columns=[
            "category",
            "severity",
            "forecast_time",
            "message",
            "measured_value"
        ]
    )

    # Remove duplicate alerts for the same category and forecast time.
    if not alert_df.empty:
        alert_df = alert_df.drop_duplicates(
            subset=["category", "forecast_time"]
        ).reset_index(drop=True)

    return alert_df


def summarize_alerts(alert_df):
    """Return counts of alerts by severity and category."""
    if alert_df.empty:
        return {
            "total_alerts": 0,
            "critical_alerts": 0,
            "high_alerts": 0,
            "moderate_alerts": 0,
            "categories": {}
        }

    severity_counts = alert_df["severity"].value_counts()

    return {
        "total_alerts": len(alert_df),
        "critical_alerts": int(severity_counts.get("Critical", 0)),
        "high_alerts": int(severity_counts.get("High", 0)),
        "moderate_alerts": int(severity_counts.get("Moderate", 0)),
        "categories": alert_df["category"].value_counts().to_dict()
    }


def save_alert_report(alert_df, filepath):
    """Save generated alerts to a CSV report."""
    alert_df.to_csv(filepath, index=False)
    return filepath

print("Weather alert system module loaded successfully!")
