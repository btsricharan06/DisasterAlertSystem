import requests


def get_weather_data():
    api_key = 'a89a60089af649be843133648251009'
    city = input('Enter the city name: ')

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ Weather data fetched successfully:")
        print(data)
    else:
        print("❌ Error fetching weather:")
        print(response.text)

#get_weather_data()


# from twilio.rest import Client
#
# # Your Twilio account credentials
# account_sid = 'ACa4972a41389f65147790495003c80c3e'
# auth_token = '59f3b6071bf163816613b5f7395cf342'
#
# # Initialize Twilio client
# client = Client(account_sid, auth_token)
#
# def send_sms(to_phone, message_body):
# #    to_phone = input('Enter your phone number: ')
#     message = client.messages.create(
#         body=message_body,
#         from_='+91 75618 83360',  #Twix number
#         to=to_phone           #User input recipient number
#     )
#     print(f"Message sent with SID: {message.sid}")
#     return message.sid
#
# send_sms('+91 99877 29556' ,"YOU ARE IN GRAVE DANGER GET TF OUT")


def sendSMS(sender_id, message, phone_number):
    api_key = 'tQocwqPh1XNFA4nkOdbSKE3e9yzG2rH5mf7RlVMDTJsuLYWj6pUr38dLWk9Ou0AnKRasIgqMZx2NmDc7'
    url = "https://www.fast2sms.com/dev/bulkV2"

    message1 = {
        "sender_id": sender_id,
        "message": message,
        "language": "english",
        "route": "v3",
        "numbers": phone_number
    }



