import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
# Sign up for a free API via Open Weather Map, place your API key within a .env file stored in the same directory as your scripts and = the API Key as 'WEATHER_API_KEY"
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    """
    Fetches real-time weather data from OpenWeather API.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"].title()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return f"""
            🌦 Weather Report for {city} 🌦
            --------------------------------
            🌤 Condition: {weather_description}
            🌡 Temperature: {temperature}°C
            💧 Humidity: {humidity}%
            💨 Wind Speed: {wind_speed} m/s
            """
        else:
            return "❌ Error: Invalid city name or API issue."

    except requests.exceptions.RequestException as e:
        return f"❌ Error: API request failed - {e}"


if __name__ == "__main__":
    city = input("Enter city name: ")
    weather_report = get_weather(city)
    print(weather_report)
