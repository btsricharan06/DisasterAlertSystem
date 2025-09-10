import requests


def get_weather_data():
    API_KEY = 'a89a60089af649be843133648251009'
    CITY = input('Enter the region name: ')

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current = data['current']

        condition = current['condition']['text']
        wind_kph = current['wind_kph']
        precip_mm = current['precip_mm']
        pressure_mb = current['pressure_mb']


        print("✅ Weather data fetched successfully:")
        print(data)
        print(f"Condition: {condition}")
        print(f"Wind Speed: {wind_kph} kph")
        print(f"Precipitation: {precip_mm} mm")
        print(f"Pressure: {pressure_mb} mb")

        if is_storm(condition, wind_kph, precip_mm, pressure_mb):
            print("⚠️ Storm likely! Sending alerts...")

        else:
            print("🌤️ Weather conditions are normal.")
    else:
        print("❌ Error fetching weather:")
        print(response.text)


def is_storm(condition, wind_kph, precip_mm, pressure_mb):
    if 'storm' in condition.lower() or 'thunder' in condition.lower():
        return True
    if wind_kph >= 50:
        return True
    if precip_mm >= 50:
        return True
    if pressure_mb <= 990:
        return True
    return False

'''
def send_sms_alerts(city, condition, wind_kph, precip_mm, pressure_mb):
    ACCOUNT_SID = 'your_account_sid_here'
    AUTH_TOKEN = 'your_auth_token_here'
    FROM_NUMBER = '+1234567890'

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    recipients = [
        '+19876543210',
        '+10987654321'
    ]

    message_body = (
        f"⚠️ Storm Alert for {city}!\n"
        f"Condition: {condition}\n"
        f"Wind Speed: {wind_kph} kph\n"
        f"Precipitation: {precip_mm} mm\n"
        f"Pressure: {pressure_mb} mb\n"
        "Stay safe and take precautions!"
    )

    for number in recipients:
        message = client.messages.create(
            body=message_body,
            from_=FROM_NUMBER,
            to=number
        )
        print(f"📩 Alert sent to {number}: SID {message.sid}")

'''
if __name__ == "__main__":

    get_weather_data()