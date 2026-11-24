# Weather Forecast & Alert Application

A Python-based weather forecasting and monitoring application with live weather data, forecast analytics, automated alerts, visualizations and an interactive Streamlit dashboard.

## Features
- Live weather data using OpenWeatherMap API
- City-based weather search
- Five-day weather forecast analysis
- Temperature and humidity analysis
- Rainfall and precipitation probability analysis
- Automated weather alerts
- Interactive Streamlit dashboard
- Weather charts and visualizations
- JSON, CSV and TXT report generation
- Offline simulation mode

## Technologies
- Python
- Pandas and NumPy
- Matplotlib
- Requests
- Streamlit
- OpenWeatherMap API

## Installation
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file in the project root.
4. Add your API key as `OPENWEATHERMAP_API_KEY=your_api_key_here`.
5. Launch the application using `streamlit run dashboard.py`.

## Offline Demo
The application includes simulated weather data for testing without live API access.

## Security
Keep your API key private. Never upload your `.env` file to GitHub.

## Project Structure
```text
Weather-Forecast-Alert-Application/
├── src/
├── data/
├── outputs/
├── images/
├── reports/
├── docs/
├── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```
