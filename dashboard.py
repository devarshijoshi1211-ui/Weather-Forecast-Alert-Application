
import sys
import json
import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from src.weather_api import WeatherAPI, WeatherAPIError
from src.data_processor import process_current_weather, process_forecast
from src.forecast_analyzer import (
    prepare_local_forecast,
    analyze_daily_forecast,
    analyze_temperature_trend,
    analyze_humidity,
    analyze_precipitation,
    summarize_weather_conditions,
    generate_forecast_insights
)
from src.alert_system import generate_weather_alerts, summarize_alerts
from src.report_generator import build_report_data, generate_all_reports
from src.simulation import (
    create_simulated_forecast,
    create_simulated_current_weather
)

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Weather Forecast & Alert Application",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Forecast & Alert Application")

st.caption(
    "Live weather monitoring, forecast analytics and intelligent alerts"
)

st.divider()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("⚙️ Dashboard Settings")

mode = st.sidebar.radio(
    "Select Data Mode",
    ["Live Weather", "Offline Demo"]
)

city = st.sidebar.text_input(
    "Enter City",
    value="Vadodara"
)

country_code = st.sidebar.text_input(
    "Country Code",
    value="IN",
    max_chars=2
)

st.sidebar.caption(
    "Offline Demo works without an API connection."
)

load_button = st.sidebar.button(
    "Load Weather Data",
    type="primary",
    use_container_width=True
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "forecast_df" not in st.session_state:
    st.session_state.forecast_df = None

if "daily_summary" not in st.session_state:
    st.session_state.daily_summary = None

if "alerts" not in st.session_state:
    st.session_state.alerts = None

if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# ---------------------------------------------------------
# LOAD WEATHER DATA
# ---------------------------------------------------------

def load_live_weather(city_name, country):
    api = WeatherAPI()
    try:
        coordinates = api.get_coordinates(city_name, country_code=country)
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]

        current_raw = api.get_current_weather(latitude, longitude)
        forecast_raw = api.get_forecast(latitude, longitude)

        current = process_current_weather(current_raw)
        forecast = process_forecast(forecast_raw)

        timezone_offset = current_raw.get("timezone", 0)
        return current, forecast, timezone_offset
    finally:
        api.close()

def load_offline_weather():
    current = create_simulated_current_weather()
    forecast = create_simulated_forecast()
    return current, forecast, 19800

if load_button:
    if mode == "Live Weather" and not city.strip():
        st.sidebar.error("Please enter a city name.")
    else:
        with st.spinner("Loading weather information..."):
            try:
                if mode == "Live Weather":
                    current, forecast, timezone_offset = load_live_weather(
                        city.strip(),
                        country_code.strip().upper()
                    )
                else:
                    current, forecast, timezone_offset = load_offline_weather()

                local_forecast = prepare_local_forecast(
                    forecast,
                    timezone_offset_seconds=timezone_offset
                )

                if "temperature" not in local_forecast.columns:
                    if "temp" in local_forecast.columns:
                        local_forecast["temperature"] = local_forecast["temp"]

                daily = analyze_daily_forecast(local_forecast)
                trend = analyze_temperature_trend(local_forecast)
                humidity = analyze_humidity(local_forecast)
                precipitation = analyze_precipitation(local_forecast)
                conditions = summarize_weather_conditions(local_forecast)
                alerts = generate_weather_alerts(local_forecast)
                alert_summary = summarize_alerts(alerts)

                report = build_report_data(
                    city=current.get("city", city),
                    current_weather=current,
                    daily_summary=daily,
                    temperature_trend=trend,
                    humidity_analysis=humidity,
                    precipitation_analysis=precipitation,
                    condition_summary=conditions,
                    alert_summary=alert_summary,
                    alerts=alerts
                )

                st.session_state.weather_data = current
                st.session_state.forecast_df = local_forecast
                st.session_state.daily_summary = daily
                st.session_state.alerts = alerts
                st.session_state.report_data = report
                st.session_state.alert_summary = alert_summary
                st.session_state.data_loaded = True

                st.success("Weather data loaded successfully!")
            except Exception as error:
                st.error(f"Unable to load weather data: {error}")

# ---------------------------------------------------------
# DASHBOARD CONTENT
# ---------------------------------------------------------

if not st.session_state.data_loaded:
    st.info(
        "Choose Live Weather or Offline Demo from the sidebar "
        "and click Load Weather Data."
    )
    st.subheader("Dashboard Features")
    col1, col2, col3 = st.columns(3)
    col1.metric("Weather Monitoring", "Live")
    col2.metric("Forecast Analysis", "5 Days")
    col3.metric("Alert Monitoring", "Enabled")
else:
    current = st.session_state.weather_data
    forecast = st.session_state.forecast_df
    daily = st.session_state.daily_summary
    alerts = st.session_state.alerts

    # -----------------------------------------------------
    # CURRENT WEATHER
    # -----------------------------------------------------
    st.header("📍 Current Weather")
    st.subheader(current.get("city", "Selected City"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{current.get('temperature', 0):.1f} °C")
    c2.metric("Feels Like", f"{current.get('feels_like', 0):.1f} °C")
    c3.metric("Humidity", f"{current.get('humidity', 0)} %")
    c4.metric("Wind Speed", f"{current.get('wind_speed', 0)} m/s")

    c5, c6, c7 = st.columns(3)
    c5.metric("Pressure", f"{current.get('pressure', 0)} hPa")
    c6.metric("Condition", str(current.get("weather_description", "N/A")).title())
    c7.metric("Cloud Cover", f"{current.get('clouds', 0)} %")

    st.divider()

    # -----------------------------------------------------
    # FORECAST
    # -----------------------------------------------------
    st.header("📈 Weather Forecast Analysis")

    chart_df = forecast.copy()
    x_column = "datetime_local" if "datetime_local" in chart_df.columns else "datetime_utc"
    chart_df[x_column] = pd.to_datetime(chart_df[x_column])

    chart_tabs = st.tabs([
        "Temperature",
        "Humidity",
        "Rainfall",
        "Rain Probability"
    ])

    with chart_tabs[0]:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(chart_df[x_column], chart_df["temperature"], marker="o")
        ax.set_title("Temperature Forecast")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=30)
        st.pyplot(fig)
        plt.close(fig)

    with chart_tabs[1]:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(chart_df[x_column], chart_df["humidity"], marker="o")
        ax.set_title("Humidity Forecast")
        ax.set_ylabel("Humidity (%)")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=30)
        st.pyplot(fig)
        plt.close(fig)

    with chart_tabs[2]:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.bar(chart_df[x_column], chart_df["rain_3h_mm"])
        ax.set_title("Rainfall Forecast")
        ax.set_ylabel("Rainfall (mm / 3 hours)")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=30)
        st.pyplot(fig)
        plt.close(fig)

    with chart_tabs[3]:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(chart_df[x_column], chart_df["probability_of_precipitation"] * 100, marker="o")
        ax.set_title("Rain Probability")
        ax.set_ylabel("Probability (%)")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=30)
        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # -----------------------------------------------------
    # DAILY SUMMARY
    # -----------------------------------------------------
    st.header("📅 Daily Forecast Summary")
    st.dataframe(daily, use_container_width=True, hide_index=True)

    st.divider()

    # -----------------------------------------------------
    # WEATHER ALERTS
    # -----------------------------------------------------
    st.header("⚠️ Weather Alerts")
    alert_summary = st.session_state.alert_summary

    a1, a2, a3 = st.columns(3)
    a1.metric("Total Alerts", alert_summary["total_alerts"])
    a2.metric("High Alerts", alert_summary["high_alerts"])
    a3.metric("Critical Alerts", alert_summary["critical_alerts"])

    if len(alerts) > 0:
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
    else:
        st.success("No weather alerts detected.")

    st.divider()

    # -----------------------------------------------------
    # TEMPERATURE TREND AND INSIGHTS
    # -----------------------------------------------------
    st.header("🔍 Weather Insights")
    trend = st.session_state.report_data["temperature_trend"]

    st.write("**Temperature Trend:**", trend.get("trend", "N/A"))
    st.write("**Temperature Change:**", f"{trend.get('temperature_change', 0):.1f} °C")

    insights = generate_forecast_insights(
        daily,
        trend,
        st.session_state.report_data["humidity_analysis"],
        st.session_state.report_data["precipitation_analysis"],
        st.session_state.report_data["weather_condition_summary"]
    )
    st.write(insights)

    st.divider()

    # -----------------------------------------------------
    # REPORT DOWNLOADS
    # -----------------------------------------------------
    st.header("📥 Download Weather Reports")
    report = st.session_state.report_data

    with tempfile.TemporaryDirectory() as temp_dir:
        report_paths = generate_all_reports(
            report,
            daily,
            alerts,
            temp_dir
        )

        files = {
            "JSON Report": Path(temp_dir) / f"{current.get('city', 'weather').lower().replace(' ', '_')}_weather_report.json",
            "Daily CSV": Path(temp_dir) / f"{current.get('city', 'weather').lower().replace(' ', '_')}_daily_report.csv",
            "Alert CSV": Path(temp_dir) / f"{current.get('city', 'weather').lower().replace(' ', '_')}_alert_report.csv",
            "Text Report": Path(temp_dir) / f"{current.get('city', 'weather').lower().replace(' ', '_')}_weather_report.txt"
        }

        download_columns = st.columns(4)
        for index, (label, path) in enumerate(files.items()):
            if path.exists():
                mime = "application/json" if path.suffix == ".json" else "text/csv" if path.suffix == ".csv" else "text/plain"
                download_columns[index].download_button(
                    label=f"Download {label}",
                    data=path.read_bytes(),
                    file_name=path.name,
                    mime=mime,
                    use_container_width=True
                )

        st.divider()
        st.caption(
            "Weather Forecast & Alert Application | "
            "Python • Streamlit • Pandas • Matplotlib • OpenWeatherMap"
        )
