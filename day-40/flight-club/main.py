from datetime import datetime as dt, timedelta

import dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

dotenv.load_dotenv()
MY_CITY = "London"

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
data_manager = DataManager()
flight_search = FlightSearch()
noti_manager = NotificationManager()

my_city_code = flight_search.get_city_code(MY_CITY)
add_user = True
while add_user:
    user_input = input("Do you want to add a new user? (y/n)\n").strip().lower()
    if user_input not in ["y", "n"]:
        print("Please answer 'Y' or 'N'")
        continue
    if user_input == "n":
        break
    data_manager.add_user()

# fill IATA Code
for city, item in data_manager.price_items.items():
    if item.city == "":
        iata_code = flight_search.get_city_code(city)
        new_item = data_manager.price_items[city]
        new_item.iataCode = iata_code
        data_manager.update_price_item(new_item)

all_dest = ",".join([item.iataCode for item in data_manager.price_items.values()])

cheapest_flights = flight_search.search_cheapest_flights_by_city(
    my_city_code,
    all_dest,
    date_from=dt.today() + timedelta(days=1),
    date_to=dt.today() + timedelta(days=180),
)


for flight in cheapest_flights:
    if flight.price < data_manager.price_items[flight.cityTo].lowestPrice:
        new_item = data_manager.price_items[flight.cityTo]
        new_item.lowestPrice = flight.price
        data_manager.update_price_item(new_item)

        noti_manager.send_email(
            flight, to_addrs=[user.email for user in data_manager.users]
        )
