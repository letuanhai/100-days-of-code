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


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    API_URL = (
        "https://api.sheety.co/fc3b6272633e38c647f286f2efc491f4/flightDeals/prices"
    )

    def __init__(self) -> None:
        self._headers = {"Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}"}
        self._items = {item.city: item for item in self._get_data()}

    @property
    def items(self) -> Dict[str, PriceItem]:
        return self._items

    def _get_data(self) -> List[PriceItem]:
        r = requests.get(url=self.API_URL, headers=self._headers)
        r.raise_for_status()
        data = r.json()["prices"]
        print(data)
        return [PriceItem.from_dict(row) for row in data]
        # return [PriceItem.from_dict(row) for row in _mock_data]

    def update_item(self, updated_item: PriceItem):
        assert (
            updated_item.city in self._items
        ), "Cannot update an item not in current data"

        body = {"price": asdict(updated_item)}
        r = requests.put(
            url=f"{self.API_URL}/{updated_item.id}", headers=self._headers, json=body
        )
        r.raise_for_status()
        print(r.text)

        self._items[updated_item.city] = updated_item


_mock_data = [
    {"city": "Paris", "iataCode": "PAR", "lowestPrice": 15, "id": 2},
    {"city": "Berlin", "iataCode": "BER", "lowestPrice": 42, "id": 3},
    {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 485, "id": 4},
    {"city": "Sydney", "iataCode": "SYD", "lowestPrice": 551, "id": 5},
    {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 95, "id": 6},
    {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 414, "id": 7},
    {"city": "New York", "iataCode": "NYC", "lowestPrice": 240, "id": 8},
    {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 260, "id": 9},
    {"city": "Cape Town", "iataCode": "CPT", "lowestPrice": 378, "id": 10},
]
