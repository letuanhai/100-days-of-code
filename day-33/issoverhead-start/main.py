import requests
from datetime import datetime, timezone
import smtplib
from collections import namedtuple
import time

MY_EMAIL = "letuanhai@live.com"
TO_EMAIL = "letuanhai1995@gmail.com"
EMAIL_PW = "ghsehyxulqdpmhon"
OUTLOOK_SMTP = "smtp-mail.outlook.com"

MY_LAT = 21.195923  # Your latitude
MY_LONG = 105.848589  # Your longitude

Point = namedtuple("Point", ["lat", "lng"])


def get_iss_pos() -> Point:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return Point(iss_latitude, iss_longitude)


# Your position is within +5 or -5 degrees of the ISS position.
def is_within_sight(pos: Point) -> bool:
    return (MY_LAT - 5 <= pos.lat <= MY_LAT + 5) and (
        MY_LONG - 5 <= pos.lng <= MY_LONG + 5
    )


def is_dark() -> bool:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    sunset_time = datetime.strptime(sunset, r"%Y-%m-%dT%H:%M:%S%z")
    sunrise_time = datetime.strptime(sunrise, r"%Y-%m-%dT%H:%M:%S%z")
    time_now = datetime.now(timezone.utc)
    print(sunset, sunset_time, sunrise, sunrise_time, time_now, sep="\n")
    return sunset_time <= time_now < sunrise_time


def send_email(iss_pos: Point):
    print("ISS is within sight!!! Sending email...")
    with smtplib.SMTP(OUTLOOK_SMTP, port=587) as conn:
        conn.starttls()
        conn.login(user=MY_EMAIL, password=EMAIL_PW)
        conn.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:Heads up! It's the ISS\n\nLook up to the sky!!! The ISS position is at latitude: {iss_pos.lat} and longitude: {iss_pos.lng}.",
        )


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    print("Checking ISS postion...")
    iss_pos = get_iss_pos()
    if is_within_sight(iss_pos) and is_dark():
        send_email(iss_pos)
    time.sleep(60)
