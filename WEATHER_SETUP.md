# Weather API Setup for Fasal Saathi

## Overview
The weather feature provides:
- Real-time weather data (temperature, humidity, rainfall)
- 7-day weather forecast
- Auto-fill annual rainfall based on state

## Setup Instructions

### Step 1: Get a Free Weather API Key

**Option A: OpenWeatherMap (Recommended)**
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to "API Keys" section
4. Copy your default API key

**Option B: WeatherAPI (Alternative)**
1. Go to https://www.weatherapi.com/
2. Sign up for a free account
3. Get your API key from the dashboard

### Step 2: Configure the API Key

Edit the `.env` file in the project root:

```bash
# For OpenWeatherMap
OPENWEATHER_API_KEY=your_actual_api_key_here

# OR for WeatherAPI
WEATHERAPI_KEY=your_actual_api_key_here
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or specifically:
```bash
pip install requests python-dotenv
```

### Step 4: Test the Setup

Run the app:
```bash
python app.py
```

Select a state and click "Fetch Weather Data" to see if it works.

## Features

### Auto-fetch on State Selection
When you select a state from the dropdown, the app automatically:
- Fetches current weather for that state
- Shows a 7-day forecast
- Pre-fills the annual rainfall field with historical averages

### Manual Weather Refresh
Click "Fetch Weather Data" button to refresh weather information.

### Auto-fill Rainfall
Click "Auto-fill from State" to set the annual rainfall to the historical average for that state.

## API Limits (Free Tiers)

### OpenWeatherMap Free
- 60 calls/minute
- 1,000,000 calls/month

### WeatherAPI Free
- 1 million calls/month
- Real-time weather
- 3-day forecast

## Troubleshooting

### "Weather API not configured"
- Make sure you added your API key to the `.env` file
- Restart the app after adding the API key
- Check that the key doesn't have spaces or extra quotes

### Weather not updating
- Check your internet connection
- Verify the API key is valid
- Try the other weather API service

### Rate limit exceeded
- Wait a minute before trying again
- Both APIs have generous free limits, but rapid testing can hit them

