


def send_sms_alerts(city, condition, wind_kph, precip_mm, pressure_mb):
    ACCOUNT_SID = 'ACa4972a41389f65147790495003c80c3e'
    AUTH_TOKEN = 'ACa4972a41389f65147790495003c80c3e'
    FROM_NUMBER = '+919999410479'

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    recipients = [
        '+919987729556',
        '+917561883360'
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

