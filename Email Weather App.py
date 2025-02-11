import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API and Email Credentials (Replace with your actual credentials)
API_KEY = os.getenv("WEATHER_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


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

            return {
                "city": city,
                "description": weather_description,
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed
            }
        else:
            return {"error": "Invalid city name or API issue"}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}


def send_email(weather_data, recipient_email):
    """
    Sends an email notification with weather details.
    """
    if "error" in weather_data:
        print("❌ Cannot send email. Error in weather data.")
        return

    # Email Content
    subject = f"Weather Report for {weather_data['city']}"
    body = f"""
    🌦 Weather Report for {weather_data['city']} 🌦

    🌤 Condition: {weather_data['description']}
    🌡 Temperature: {weather_data['temperature']}°C
    💧 Humidity: {weather_data['humidity']}%
    💨 Wind Speed: {weather_data['wind_speed']} m/s

    Stay safe and have a great day! 🌍
    """

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Email sending failed: {e}")


if __name__ == "__main__":
    city = input("Enter city name: ")
    recipient_email = input("Enter your email address: ")

    weather_data = get_weather(city)

    if "error" in weather_data:
        print(f"❌ Error: {weather_data['error']}")
    else:
        print(f"✅ Weather report for {city} retrieved successfully!")
        send_email(weather_data, recipient_email)
