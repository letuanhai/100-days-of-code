from __future__ import annotations

from dataclasses import dataclass, InitVar, field
from datetime import datetime, timedelta
from typing import Dict


@dataclass
class FlightData:
    """This class is responsible for structuring the flight data."""

    cityFrom: str
    cityTo: str
    flyFrom: str
    flyTo: str
    price: float
    local_departure: InitVar[str]
    nightsInDest: InitVar[int]
    from_date: datetime = field(init=False)
    to_date: datetime = field(init=False)

    def __post_init__(self, local_departure, nightsInDest):
        self.from_date = datetime.strptime(local_departure, r"%Y-%m-%dT%H:%M:%S.%fZ")
        self.to_date = self.from_date + timedelta(days=nightsInDest)

    @classmethod
    def from_dict(cls, arg: Dict) -> FlightData:
        """Method to create a new instance from a dict, ignoring redundant keys."""
        # Annotate return type as current class: https://stackoverflow.com/a/49872353/12146204
        return cls(
            **{k: v for k, v in arg.items() if k in cls.__dataclass_fields__.keys()}
        )
