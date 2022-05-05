import os

from twilio.rest import Client

from flight_data import FlightData


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    _from_number = "+16165801062"
    _to_number = "+84969272995"

    def __init__(self) -> None:
        account_sid = os.environ["TWILIO_ACC"]
        auth_token = os.environ["TWILIO_TOKEN"]
        self._client = Client(account_sid, auth_token)

    def send_flight_noti(self, f: FlightData):
        msg = self._client.messages.create(
            to=self._to_number,
            from_=self._from_number,
            body=(
                f"Low price alert! Only ${f.price:,.2f} to fly "
                f"from {f.cityFrom}-{f.flyFrom} to {f.cityTo}-{f.flyTo}, "
                f"from {f.from_date.strftime('%Y-%m-%d')} to {f.to_date.strftime('%Y-%m-%d')}.",
            ),
        )
        print(msg.sid)
