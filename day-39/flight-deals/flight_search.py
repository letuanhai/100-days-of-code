import os
from datetime import datetime
from typing import List

import requests

from flight_data import FlightData


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    _API_URL = "https://tequila-api.kiwi.com"
    _LOCATION_ENDPOINT = r"/locations/query"
    _FLIGHT_SEARCH_ENDPOINT = r"/v2/search"
    _date_format = r"%d/%m/%Y"

    def __init__(self) -> None:
        self._headers = {"apikey": os.environ["FLIGHT_KEY"]}

    def get_city_code(self, city_name: str) -> str:
        params = {"term": city_name, "locale": "en-us", "location_types": "city"}
        r = requests.get(
            url=self._API_URL + self._LOCATION_ENDPOINT,
            headers=self._headers,
            params=params,
        )
        r.raise_for_status()
        return r.json()["locations"][0]["code"]

    def search_flight_by_city(
        self, from_code: str, to_code: str, date_from: datetime, date_to: datetime
    ) -> List[FlightData]:
        params = {
            "fly_from": from_code,
            "fly_to": to_code,
            "date_from": date_from.strftime(self._date_format),
            "date_to": date_to.strftime(self._date_format),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "USD",
        }

        r = requests.get(
            url=self._API_URL + self._FLIGHT_SEARCH_ENDPOINT,
            headers=self._headers,
            params=params,
        )
        r.raise_for_status()
        data = r.json()["data"]
        return [FlightData.from_dict(flight) for flight in data]


# f = FlightSearch()
# print(f.get_city_code("London"))
