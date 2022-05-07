from __future__ import annotations

import os
from typing import Dict, List
from dataclasses import dataclass, asdict

import requests


@dataclass
class PriceItem:
    """Class represent each row of Prices table."""

    city: str
    iataCode: str
    lowestPrice: float
    id: int

    @classmethod
    def from_dict(cls, arg: Dict) -> PriceItem:
        """Method to create a new instance from a dict, ignoring redundant keys."""
        # Annotate return type as current class: https://stackoverflow.com/a/49872353/12146204
        return cls(
            **{k: v for k, v in arg.items() if k in cls.__dataclass_fields__.keys()}
        )


@dataclass
class User:
    firstName: str
    lastName: str
    email: str

    @classmethod
    def from_dict(cls, arg: Dict) -> User:
        return cls(
            **{k: v for k, v in arg.items() if k in cls.__dataclass_fields__.keys()}
        )


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    PRICE_API_ENDPOINT = (
        "https://api.sheety.co/fc3b6272633e38c647f286f2efc491f4/flightDeals/prices"
    )
    USER_API_ENDPOINT = (
        "https://api.sheety.co/fc3b6272633e38c647f286f2efc491f4/flightDeals/users"
    )

    def __init__(self) -> None:
        self._headers = {"Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}"}
        self._price_items = {item.city: item for item in self._get_price_data()}
        self._user_data = self._get_user_data()

    @property
    def price_items(self) -> Dict[str, PriceItem]:
        return self._price_items

    @property
    def users(self) -> List[User]:
        return self._user_data

    def _get_price_data(self) -> List[PriceItem]:
        # r = requests.get(url=self.PRICE_API_ENDPOINT, headers=self._headers)
        # r.raise_for_status()
        # data = r.json()["prices"]
        # print(data)
        # return [PriceItem.from_dict(row) for row in data]
        return [PriceItem.from_dict(row) for row in _mock_price_data]

    def _get_user_data(self):
        # r = requests.get(url=self.USER_API_ENDPOINT, headers=self._headers)
        # r.raise_for_status()
        # data = r.json()["users"]
        # print(data)
        # return [User.from_dict(row) for row in data]
        return [User.from_dict(row) for row in _mock_user_data]

    def add_user(self):
        print(
            """Welcome to Flight Club.
We find the best flight deals and email you."""
        )
        first_name = input("What is your first name?\n").strip()
        last_name = input("What is your last name?\n").strip()
        email = input("What is your email?\n").strip().lower()
        confirm_email = input("Type your email again.\n").strip().lower()

        if email == confirm_email:
            new_user = User(first_name, last_name, email)
            self._user_data.append(new_user)
            self._upload_user(new_user)
            print("You're in the club")
        else:
            print("Email does not match!!")

    def _upload_user(self, new_user: User):
        body = {
            "user": {
                "firstName": new_user.firstName,
                "lastName": new_user.lastName,
                "email": new_user.email,
            }
        }
        r = requests.post(url=self.USER_API_ENDPOINT, headers=self._headers, json=body)
        r.raise_for_status()
        # print(r.text)

    def update_price_item(self, updated_item: PriceItem):
        assert (
            updated_item.city in self._price_items
        ), "Cannot update an item not in current data"

        body = {"price": asdict(updated_item)}
        r = requests.put(
            url=f"{self.PRICE_API_ENDPOINT}/{updated_item.id}",
            headers=self._headers,
            json=body,
        )
        r.raise_for_status()
        # print(r.text)

        self._price_items[updated_item.city] = updated_item


_mock_price_data = [
    {"city": "Paris", "iataCode": "PAR", "lowestPrice": 999, "id": 2},
    {"city": "Berlin", "iataCode": "BER", "lowestPrice": 999, "id": 3},
    {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 999, "id": 4},
    {"city": "Sydney", "iataCode": "SYD", "lowestPrice": 999, "id": 5},
    {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 999, "id": 6},
    {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 999, "id": 7},
    {"city": "New York", "iataCode": "NYC", "lowestPrice": 999, "id": 8},
    {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 999, "id": 9},
    {"city": "Cape Town", "iataCode": "CPT", "lowestPrice": 999, "id": 10},
]

_mock_user_data = [
    {
        "firstName": "Hai",
        "lastName": "Le",
        "email": "letuanhai1995@gmail.com",
    }
]
