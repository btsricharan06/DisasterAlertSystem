import time
import random

# --- CONFIGURATION ---
CITY = "YourVillage"
ALERT_PHONE_NUMBER = "+911234567890"

# --- FUNCTIONS ---

def get_weather():
    """Simulate fetching weather data from IndianAPI"""
    # Randomly generate weather conditions for demo
    conditions = ["Clear", "Clouds", "Heavy Rain", "Thunderstorm", "Tornado"]
    weather_data = {
        "city": CITY,
        "temperature": random.randint(20, 40),  # °C
        "humidity": random.randint(40, 90),    # %
        "wind_speed": random.randint(5, 25),   # m/s
        "condition": random.choice(conditions)
    }
    print(f"🔹 Fetched weather data: {weather_data}")
    return weather_data

def is_weather_dangerous(weather_data):
    """Check if conditions are dangerous"""
    wind_speed = weather_data["wind_speed"]
    condition = weather_data["condition"]

    if wind_speed > 15:
        return f"⚠️ ALERT: High Wind Speed ({wind_speed} m/s)"
    if condition in ["Thunderstorm", "Tornado", "Heavy Rain"]:
        return f"⚠️ ALERT: Dangerous Weather ({condition})"
    return None

def send_sms(message):
    """Simulate sending SMS"""
    print(f"📩 SMS sent to {ALERT_PHONE_NUMBER}: {message}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🌐 Disaster Alert System Demo Started...")
    for _ in range(5):  # Run 5 demo cycles
        weather = get_weather()
        alert_message = is_weather_dangerous(weather)
        if alert_message:
            print("Sending alert:", alert_message)
            send_sms(alert_message)
        else:
            print("Weather is safe.")
        print("-" * 50)
        time.sleep(2)  # Short wait for demo
