"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent
import requests


MODEL = "gemini-2.5-flash"

API_KEY_WEATHER=''


def get_weather(city: str) -> dict:
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "q": city,
        "key": API_KEY_WEATHER,
        "aqi": 'false'  # Use "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        api_response=data["current"]
        return { "temperature_celsius": api_response.get("temp_c"),
        "feels_like_celsius": api_response.get("feelslike_c"),
        "condition": api_response.get("condition", {}).get("text"),
        "humidity_percent": api_response.get("humidity"),
        "wind": {
            "speed_kph": api_response.get("wind_kph"),
            "direction": api_response.get("wind_dir")
        },
        "precipitation_mm": api_response.get("precip_mm"),
        "visibility_km": api_response.get("vis_km"),
        "uv_index": api_response.get("uv"),
        "last_updated": api_response.get("last_updated"),
        "is_daytime": bool(api_response.get("is_day"))
        }
    else:
      return {"error": f"Failed to fetch weather. Status: {response.status_code}"}


import requests
def get_weather_forecast(city: str, days: str) -> dict:
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "q": city,
        "key": API_KEY_WEATHER,
        "aqi": 'false',  # Use "imperial" for Fahrenheit
        "days": days,
        "alerts": "yes"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        day_data = data["forecast"]["forecastday"][0]["day"]
        date = data["forecast"]["forecastday"][0]["date"]
        return {
            "condition": day_data["condition"]["text"],
            "max_temp_c": day_data["maxtemp_c"],
            "min_temp_c": day_data["mintemp_c"],
            "chance_of_rain": day_data["daily_chance_of_rain"],
            "total_precip_mm": day_data["totalprecip_mm"],
            "avg_humidity": day_data["avghumidity"],
            "uv_index": day_data["uv"]
        }
    else:
      return {"error": f"Failed to fetch weather. Status: {response.status_code}"}


weather_forecast_agent = Agent(
    name="weather_forecast_agent",
    model=MODEL,
    description="Provides current weather and multi-day forecast information for specific cities or regions.",
    instruction="""
You are a weather assistant for farmers and agri-users.

Your job is to:
- Understand if the user is asking for **current weather** or a **forecast**.
- If it's a **current weather** request (e.g., "What’s the weather in Delhi?"), use the `get_weather(city)` tool.
- If it's a **forecast** request (e.g., "Weather forecast for Pune for 3 days"), use the `get_weather_forecast(city, days)` tool with both the city and number of days as arguments.

Guidelines:
- Extract the **city name** and **forecast duration (if any)** from the user’s message.
- Assume `days = "1"` if the user asks for “forecast” but doesn’t mention a duration.
- If the tool call fails, politely inform the user with the error message.
- If successful:
  - For current weather: show temperature, condition, humidity, and wind info in simple language.
  - For forecast: show date, condition, temperature range, humidity, rain chance, and UV index in bullet format.

Examples:
1. "Kal barish hogi kya Lucknow mein?" → `get_weather_forecast("Lucknow", "1")`
2. "Weather in Bengaluru today" → `get_weather("Bengaluru")`
3. "Give me 3-day forecast for Nagpur" → `get_weather_forecast("Nagpur", "3")`
4. "Aaj ka mausam kya hai Hyderabad mein?" → `get_weather("Hyderabad")`

Always be concise and friendly. Avoid technical jargon unless the user used it.
""",
    tools=[get_weather, get_weather_forecast]
)

