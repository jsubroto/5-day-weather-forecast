# 5 Day Weather Forecast
Python application which calls the [OpenWeatherMap API](https://openweathermap.org/api) to get a 5-day weather forecast, partitioned into 3-hour blocks.

### Input
* City Name
* or Zip Code

### Output
* City name
* Country code
* Datetime (*YYYY-MM-DD HH:MM UTC*)
* Weather condition
* Temperature (°C and °F)
* Humidity

## Getting Started

1. **Get an API key**  
   Sign up and get an **API KEY**: https://openweathermap.org/api

2. **Create a `.env` file** in the project root:
   ~~~env
   OPENWEATHER_API_KEY=your-api-key-here
   ~~~

3. **Run the app**  
   Using [uv](https://docs.astral.sh/uv):
   ~~~bash
   uv run --env-file .env main.py
   ~~~

4. **Read the API docs**  
   5-day forecast: https://openweathermap.org/forecast5

