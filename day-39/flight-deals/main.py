from datetime import datetime as dt, timedelta

import dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

dotenv.load_dotenv()
MY_CITY = "London"

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
current_data = DataManager()
fs = FlightSearch()
sms = NotificationManager()

my_city_code = fs.get_city_code(MY_CITY)

# fill IATA Code
for city, item in current_data.items.items():
    if item.city == "":
        iata_code = fs.get_city_code(city)
        new_item = current_data.items[city]
        new_item.iataCode = iata_code
        current_data.update_item(new_item)

all_dest = ",".join([item.iataCode for item in current_data.items.values()])

cheapest_flights = fs.search_flight_by_city(
    my_city_code,
    all_dest,
    date_from=dt.today() + timedelta(days=1),
    date_to=dt.today() + timedelta(days=180),
)

for flight in cheapest_flights:
    if flight.price < current_data.items[flight.cityTo].lowestPrice:
        new_item = current_data.items[flight.cityTo]
        new_item.lowestPrice = flight.price
        current_data.update_item(new_item)

        sms.send_flight_noti(flight)
