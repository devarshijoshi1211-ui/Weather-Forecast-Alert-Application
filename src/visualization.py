
# ============================================================
# WEATHER FORECAST & ALERT APPLICATION
# PHASE 8: WEATHER VISUALIZATION
# FILE: src/visualization.py
# ============================================================

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def prepare_chart_data(df):
    """Validate and prepare forecast data for chart generation."""
    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    data = df.copy()

    if "datetime_local" in data.columns:
        data["chart_time"] = pd.to_datetime(data["datetime_local"])
    elif "datetime_utc" in data.columns:
        data["chart_time"] = pd.to_datetime(data["datetime_utc"], utc=True)
    else:
        raise ValueError("No forecast datetime column found.")

    data = data.sort_values("chart_time").reset_index(drop=True)
    return data


def save_chart(fig, filepath):
    """Save a chart and close its figure to release memory."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        filepath,
        dpi=150,
        bbox_inches="tight",
        facecolor="white"
    )
    plt.close(fig)
    return filepath


def plot_temperature_forecast(df, output_dir):
    data = prepare_chart_data(df)
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        data["chart_time"],
        data["temperature"],
        marker="o",
        linewidth=2,
        label="Temperature"
    )

    ax.fill_between(
        data["chart_time"],
        data["temperature"],
        alpha=0.15
    )

    ax.set_title("Weather Forecast - Temperature Trend", fontsize=15)
    ax.set_xlabel("Forecast Time")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()

    return save_chart(
        fig, Path(output_dir) / "temperature_forecast.png"
    )


def plot_humidity_forecast(df, output_dir):
    data = prepare_chart_data(df)

    if "humidity" not in data.columns:
        raise ValueError("Humidity column is missing.")

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        data["chart_time"],
        data["humidity"],
        marker="o",
        linewidth=2,
        label="Humidity"
    )

    ax.axhline(
        80,
        linestyle="--",
        linewidth=1.5,
        label="High humidity reference (80%)"
    )

    ax.set_title("Weather Forecast - Humidity Trend", fontsize=15)
    ax.set_xlabel("Forecast Time")
    ax.set_ylabel("Humidity (%)")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()

    return save_chart(
        fig, Path(output_dir) / "humidity_forecast.png"
    )


def plot_rainfall_forecast(df, output_dir):
    data = prepare_chart_data(df)

    rainfall = data.get(
        "rain_3h_mm", pd.Series(0, index=data.index)
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        data["chart_time"],
        rainfall,
        width=0.08,
        label="Forecast rainfall"
    )

    ax.set_title("Weather Forecast - Rainfall", fontsize=15)
    ax.set_xlabel("Forecast Time")
    ax.set_ylabel("Rainfall (mm per 3 hours)")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()

    return save_chart(
        fig, Path(output_dir) / "rainfall_forecast.png"
    )


def plot_rain_probability(df, output_dir):
    data = prepare_chart_data(df)

    probability = data.get(
        "probability_of_precipitation",
        pd.Series(0, index=data.index)
    ).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        data["chart_time"],
        probability,
        marker="o",
        linewidth=2,
        label="Rain probability"
    )

    ax.axhline(
        60,
        linestyle="--",
        linewidth=1.5,
        label="Alert threshold (60%)"
    )

    ax.set_title("Weather Forecast - Rain Probability", fontsize=15)
    ax.set_xlabel("Forecast Time")
    ax.set_ylabel("Probability (%)")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()

    return save_chart(
        fig, Path(output_dir) / "rain_probability_forecast.png"
    )


def create_weather_dashboard(df, output_dir):
    data = prepare_chart_data(df)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Temperature
    axes[0, 0].plot(
        data["chart_time"],
        data["temperature"],
        marker="o",
        linewidth=2
    )
    axes[0, 0].set_title("Temperature Forecast")
    axes[0, 0].set_ylabel("Temperature (°C)")
    axes[0, 0].grid(True, alpha=0.3)

    # Humidity
    axes[0, 1].plot(
        data["chart_time"],
        data["humidity"],
        marker="o",
        linewidth=2
    )
    axes[0, 1].set_title("Humidity Forecast")
    axes[0, 1].set_ylabel("Humidity (%)")
    axes[0, 1].set_ylim(0, 105)
    axes[0, 1].grid(True, alpha=0.3)

    # Rainfall
    rainfall = data.get(
        "rain_3h_mm", pd.Series(0, index=data.index)
    ).fillna(0)

    axes[1, 0].bar(data["chart_time"], rainfall)
    axes[1, 0].set_title("Rainfall Forecast")
    axes[1, 0].set_ylabel("Rainfall (mm / 3 hours)")
    axes[1, 0].grid(axis="y", alpha=0.3)

    # Rain probability
    probability = data.get(
        "probability_of_precipitation",
        pd.Series(0, index=data.index)
    ).fillna(0) * 100

    axes[1, 1].plot(
        data["chart_time"],
        probability,
        marker="o",
        linewidth=2
    )
    axes[1, 1].set_title("Rain Probability")
    axes[1, 1].set_ylabel("Probability (%)")
    axes[1, 1].set_ylim(0, 105)
    axes[1, 1].grid(True, alpha=0.3)

    for ax in axes.flat:
        ax.set_xlabel("Forecast Time")
        ax.tick_params(axis="x", rotation=30)

    fig.suptitle(
        "Weather Forecast - Complete Analysis Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    return save_chart(
        fig, Path(output_dir) / "complete_weather_dashboard.png"
    )


def generate_all_weather_charts(df, output_dir):
    """Generate all five project visualizations."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = [
        plot_temperature_forecast(df, output_dir),
        plot_humidity_forecast(df, output_dir),
        plot_rainfall_forecast(df, output_dir),
        plot_rain_probability(df, output_dir),
        create_weather_dashboard(df, output_dir)
    ]

    return generated_files


print("Weather visualization module loaded successfully!")
