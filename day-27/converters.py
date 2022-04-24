def km_to_mile(km: float) -> str:
    return f"{km} km are {round(km / 1.609, 2)} miles."


def mile_to_km(mile: float) -> str:
    return f"{mile} miles are {round(mile * 1.609, 2)} km."


def kg_to_pound(kg: float) -> str:
    return f"{kg} kg are {round(kg * 2.205, 2)} pounds."


def pound_to_kg(pound: float) -> str:
    return f"{pound} pounds are {round(pound / 2.205, 2)} kg."
