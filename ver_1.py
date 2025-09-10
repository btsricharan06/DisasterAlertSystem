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

if __name__ == "__main__":

    get_weather_data()