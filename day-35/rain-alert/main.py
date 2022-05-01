import os

import requests
from twilio.rest import Client


def will_rain() -> bool:
    API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

    api_key = os.getenv("OWM_API_KEY")

    params = {
        "lat": 21.195923,
        "lon": 105.848589,
        "units": "metric",
        "appid": api_key,
        "exclude": "current,minutely,daily",
    }

    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()

    hourly_data = response.json()["hourly"]

    weather_ids = [hour["weather"][0]["id"] for hour in hourly_data[:12]]

    if any(int(w_id) < 700 for w_id in weather_ids):
        return True
    return False


def send_sms():
    account_sid = os.getenv("TWILIO_ACC")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_number = "+16165801062"
    to_number = "+84969272995"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Hôm nay trời mưa đó, nhớ mang ☔ nha!",
        from_=from_number,
        to=to_number,
    )
    print(message.sid)


if will_rain():
    send_sms()
