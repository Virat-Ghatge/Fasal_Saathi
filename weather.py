"""
Weather module for Fasal Saathi
Fetches real-time weather data and forecasts
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# API Keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY', '')

# State coordinates for major Indian cities
STATE_COORDINATES = {
    "Andhra Pradesh": (15.9129, 79.7400),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Assam": (26.2006, 92.9376),
    "Bihar": (25.0961, 85.3131),
    "Chhattisgarh": (21.2787, 81.8661),
    "Delhi": (28.7041, 77.1025),
    "Goa": (15.2993, 74.1240),
    "Gujarat": (22.2587, 71.1924),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Jammu and Kashmir": (33.7782, 76.5762),
    "Jharkhand": (23.6102, 85.2799),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139),
    "Manipur": (24.6637, 93.9063),
    "Meghalaya": (25.4670, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Nagaland": (26.1584, 94.5624),
    "Odisha": (20.9517, 85.0985),
    "Puducherry": (11.9416, 79.8083),
    "Punjab": (31.1471, 75.3412),
    "Sikkim": (27.5330, 88.5122),
    "Tamil Nadu": (11.1271, 78.6569),
    "Telangana": (17.1232, 79.2088),
    "Tripura": (23.9408, 91.9882),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttarakhand": (30.0668, 79.0193),
    "West Bengal": (22.9868, 87.8550)
}

def get_current_weather(state):
    """
    Get current weather data for a state
    Returns: dict with temperature, humidity, rainfall, description
    """
    if state not in STATE_COORDINATES:
        return None

    lat, lon = STATE_COORDINATES[state]

    # Try OpenWeatherMap first
    if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_api_key_here':
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'rainfall': data.get('rain', {}).get('1h', 0),  # Rain in last hour in mm
                    'description': data['weather'][0]['description'],
                    'source': 'OpenWeatherMap'
                }
        except Exception as e:
            print(f"OpenWeatherMap error: {e}")

    # Fallback to WeatherAPI
    if WEATHERAPI_KEY and WEATHERAPI_KEY != 'your_api_key_here':
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={lat},{lon}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['current']['temp_c'],
                    'humidity': data['current']['humidity'],
                    'rainfall': data['current'].get('precip_mm', 0),
                    'description': data['current']['condition']['text'],
                    'source': 'WeatherAPI'
                }
        except Exception as e:
            print(f"WeatherAPI error: {e}")

    return None

def get_forecast(state, days=7):
    """
    Get weather forecast for a state
    Returns: list of daily forecasts
    """
    if state not in STATE_COORDINATES:
        return None

    lat, lon = STATE_COORDINATES[state]

    # Try WeatherAPI (better for forecasts)
    if WEATHERAPI_KEY and WEATHERAPI_KEY != 'your_api_key_here':
        try:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={lat},{lon}&days={days}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                forecast = []
                for day in data['forecast']['forecastday']:
                    forecast.append({
                        'date': day['date'],
                        'temp_max': day['day']['maxtemp_c'],
                        'temp_min': day['day']['mintemp_c'],
                        'rainfall': day['day'].get('totalprecip_mm', 0),
                        'humidity': day['day'].get('avghumidity', 0),
                        'description': day['day']['condition']['text'],
                        'chance_of_rain': day['day'].get('daily_chance_of_rain', 0)
                    })
                return forecast
        except Exception as e:
            print(f"WeatherAPI forecast error: {e}")

    # Fallback to OpenWeatherMap
    if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_api_key_here':
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Group by day
                daily_data = {}
                for item in data['list']:
                    date = item['dt_txt'][:10]
                    if date not in daily_data:
                        daily_data[date] = {
                            'temps': [],
                            'rainfall': 0,
                            'humidity': []
                        }
                    daily_data[date]['temps'].append(item['main']['temp'])
                    daily_data[date]['humidity'].append(item['main']['humidity'])
                    if 'rain' in item and '3h' in item['rain']:
                        daily_data[date]['rainfall'] += item['rain']['3h']

                forecast = []
                for date, values in list(daily_data.items())[:days]:
                    forecast.append({
                        'date': date,
                        'temp_max': max(values['temps']),
                        'temp_min': min(values['temps']),
                        'rainfall': values['rainfall'],
                        'humidity': sum(values['humidity']) / len(values['humidity']),
                        'description': 'N/A',
                        'chance_of_rain': 0
                    })
                return forecast
        except Exception as e:
            print(f"OpenWeatherMap forecast error: {e}")

    return None

def get_annual_rainfall_estimate(state):
    """
    Get estimated annual rainfall based on historical data for the state
    Returns: approximate annual rainfall in mm
    """
    # Historical average rainfall data for Indian states
    state_rainfall = {
        "Andhra Pradesh": 1000,
        "Arunachal Pradesh": 2500,
        "Assam": 2000,
        "Bihar": 1200,
        "Chhattisgarh": 1400,
        "Delhi": 800,
        "Goa": 3000,
        "Gujarat": 800,
        "Haryana": 600,
        "Himachal Pradesh": 1500,
        "Jammu and Kashmir": 700,
        "Jharkhand": 1400,
        "Karnataka": 1200,
        "Kerala": 3000,
        "Madhya Pradesh": 1100,
        "Maharashtra": 1200,
        "Manipur": 1800,
        "Meghalaya": 1200,
        "Mizoram": 2500,
        "Nagaland": 2000,
        "Odisha": 1500,
        "Puducherry": 1400,
        "Punjab": 600,
        "Sikkim": 3500,
        "Tamil Nadu": 1000,
        "Telangana": 900,
        "Tripura": 2200,
        "Uttar Pradesh": 900,
        "Uttarakhand": 1500,
        "West Bengal": 1600
    }

    return state_rainfall.get(state, 1200)  # Default 1200mm

def format_weather_for_display(weather_data):
    """Format weather data for UI display"""
    if not weather_data:
        return "Weather data unavailable"

    return (f"🌡️ Temperature: {weather_data['temperature']:.1f}°C\n"
            f"💧 Humidity: {weather_data['humidity']}%\n"
            f"🌧️ Recent Rain: {weather_data['rainfall']:.1f}mm\n"
            f"☁️ Condition: {weather_data['description']}")

def format_forecast_for_display(forecast):
    """Format forecast for UI display"""
    if not forecast:
        return "Forecast unavailable"

    display = "7-Day Forecast:\n\n"
    for day in forecast[:7]:
        display += (f"📅 {day['date']}: {day['temp_max']:.1f}°C / {day['temp_min']:.1f}°C\n"
                   f"   🌧️ Rain: {day['rainfall']:.1f}mm ({day.get('chance_of_rain', 0)}%)\n"
                   f"   ☁️ {day['description']}\n\n")

    return display

# Test if API keys are configured
def check_api_keys():
    """Check if weather API keys are configured"""
    if (OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_api_key_here') or \
       (WEATHERAPI_KEY and WEATHERAPI_KEY != 'your_api_key_here'):
        return True
    return False
