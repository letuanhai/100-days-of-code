import os
import smtplib
from typing import List

from twilio.rest import Client

from flight_data import FlightData


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def send_sms(self, f: FlightData):
        from_number = "+16165801062"
        to_number = "+84969272995"
        client = Client(os.environ["TWILIO_ACC"], os.environ["TWILIO_TOKEN"])

        msg = client.messages.create(
            to=to_number,
            from_=from_number,
            body=(
                f"Low price alert! Only ${f.price:,.2f} to fly "
                f"from {f.cityFrom}-{f.flyFrom} to {f.cityTo}-{f.flyTo}, "
                f"from {f.from_date.strftime('%Y-%m-%d')} to {f.to_date.strftime('%Y-%m-%d')}."
            ),
        )
        print(msg.sid)

    def send_email(self, f: FlightData, to_addrs: List[str]):
        MY_EMAIL = "letuanhai@live.com"
        EMAIL_PW = "ghsehyxulqdpmhon"
        OUTLOOK_SMTP = "smtp-mail.outlook.com"

        if len(to_addrs) < 1:
            raise Exception("Empty to_addr list!")

        with smtplib.SMTP(OUTLOOK_SMTP, port=587) as conn:
            conn.starttls()
            conn.login(user=MY_EMAIL, password=EMAIL_PW)
            conn.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=to_addrs,
                msg=(
                    f"Subject:New Low Price Flight!\n\n"
                    f"Low price alert! Only ${f.price:,.2f} to fly "
                    f"from {f.cityFrom}-{f.flyFrom} to {f.cityTo}-{f.flyTo}, "
                    f"from {f.from_date.strftime('%Y-%m-%d')} to {f.to_date.strftime('%Y-%m-%d')}."
                ),
            )
