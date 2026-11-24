
# ============================================================
# WEATHER FORECAST & ALERT APPLICATION
# PHASE 9: WEATHER REPORT GENERATION
# FILE: src/report_generator.py
# ============================================================

import json
from pathlib import Path
from datetime import datetime, date, timezone
import pandas as pd

def json_safe(value):
    """Convert Pandas, NumPy, and standard datetime/date values into JSON-compatible values."""
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]

    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()

    if hasattr(value, "item"):
        return json_safe(value.item())

    if pd.isna(value):
        return None

    return value

def build_report_data(
    city,
    current_weather,
    daily_summary,
    temperature_trend,
    humidity_analysis,
    precipitation_analysis,
    condition_summary,
    alert_summary,
    alerts
):
    """Combine all project outputs into one report structure."""
    report = {
        "report_metadata": {
            "application": "Weather Forecast & Alert Application",
            "city": city,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "forecast_source": "OpenWeatherMap API"
        },
        "current_weather": current_weather,
        "daily_forecast_summary": daily_summary.to_dict(orient="records"),
        "temperature_trend": temperature_trend,
        "humidity_analysis": humidity_analysis,
        "precipitation_analysis": precipitation_analysis,
        "weather_condition_summary": condition_summary,
        "alert_summary": alert_summary,
        "alerts": alerts.to_dict(orient="records")
    }
    return json_safe(report)

def generate_json_report(report_data, filepath):
    """Write the complete report as formatted JSON."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as file:
        json.dump(
            json_safe(report_data),
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )
    return filepath

def generate_daily_csv_report(daily_summary, filepath):
    """Save daily forecast summaries as CSV."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    daily_summary.to_csv(filepath, index=False)
    return filepath

def generate_alert_csv_report(alerts, filepath):
    """Save generated alerts as CSV."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    alerts.to_csv(filepath, index=False)
    return filepath

def generate_text_report(report_data, filepath):
    """Create a readable text version of the weather report."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    metadata = report_data["report_metadata"]
    current = report_data["current_weather"]
    trend = report_data["temperature_trend"]
    humidity = report_data["humidity_analysis"]
    precipitation = report_data["precipitation_analysis"]
    alert_summary = report_data["alert_summary"]

    lines = [
        "=" * 70,
        "WEATHER FORECAST & ALERT APPLICATION",
        "WEATHER ANALYSIS REPORT",
        "=" * 70,
        "",
        f"City: {metadata['city']}",
        f"Generated at (UTC): {metadata['generated_at_utc']}",
        f"Data source: {metadata['forecast_source']}",
        "",
        "-" * 70,
        "CURRENT WEATHER",
        "-" * 70
    ]

    for key, value in current.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")

    lines.extend([
        "",
        "-" * 70,
        "TEMPERATURE TREND",
        "-" * 70,
        f"Starting temperature: {trend['starting_temperature']} °C",
        f"Ending temperature: {trend['ending_temperature']} °C",
        f"Temperature change: {trend['temperature_change']} °C",
        f"Trend: {trend['trend']}",
        "",
        "-" * 70,
        "HUMIDITY ANALYSIS",
        "-" * 70
    ])

    for key, value in humidity.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")

    lines.extend([
        "",
        "-" * 70,
        "PRECIPITATION ANALYSIS",
        "-" * 70
    ])

    for key, value in precipitation.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")

    lines.extend([
        "",
        "-" * 70,
        "DAILY FORECAST SUMMARY",
        "-" * 70
    ])

    for day in report_data["daily_forecast_summary"]:
        lines.append(
            f"{day['forecast_date']}: "
            f"Average {day['average_temperature']} °C, "
            f"Maximum {day['maximum_temperature']} °C, "
            f"Minimum {day['minimum_temperature']} °C"
        )

    lines.extend([
        "",
        "-" * 70,
        "WEATHER CONDITIONS",
        "-" * 70
    ])

    for condition, count in report_data["weather_condition_summary"].items():
        lines.append(f"{condition}: {count} intervals")

    lines.extend([
        "",
        "-" * 70,
        "WEATHER ALERT SUMMARY",
        "-" * 70
    ])

    for key, value in alert_summary.items():
        if key != "categories":
            lines.append(f"{key.replace('_', ' ').title()}: {value}")

    for category, count in alert_summary.get("categories", {}).items():
        lines.append(f"{category}: {count}")

    lines.extend([
        "",
        "INDIVIDUAL ALERTS",
        "-" * 70
    ])

    if not report_data["alerts"]:
        lines.append("No weather alerts generated.")
    else:
        for number, alert in enumerate(report_data["alerts"], start=1):
            lines.append(
                f"{number}. [{alert['severity']}] "
                f"{alert['category']}: {alert['message']}"
            )
            lines.append(f"   Forecast time: {alert['forecast_time']}")

    lines.extend([
        "",
        "=" * 70,
        "END OF WEATHER REPORT",
        "=" * 70
    ])

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath

def generate_all_reports(report_data, daily_summary, alerts, output_dir):
    """Generate all report files and return their paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    city = report_data["report_metadata"]["city"].lower()
    city = "".join(
        character if character.isalnum() else "_"
        for character in city
    ).strip("_")

    json_path = generate_json_report(
        report_data,
        output_dir / f"{city}_weather_report.json"
    )

    daily_csv_path = generate_daily_csv_report(
        daily_summary,
        output_dir / f"{city}_daily_report.csv"
    )

    alert_csv_path = generate_alert_csv_report(
        alerts,
        output_dir / f"{city}_alert_report.csv"
    )

    text_path = generate_text_report(
        report_data,
        output_dir / f"{city}_weather_report.txt"
    )

    return [
        json_path,
        daily_csv_path,
        alert_csv_path,
        text_path
    ]

print("Weather report generation module loaded successfully!")
