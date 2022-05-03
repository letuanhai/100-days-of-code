import os
from datetime import datetime as dt
from typing import Dict, List

import requests
import dotenv

dotenv.load_dotenv()


def get_exercise_data() -> List[Dict]:
    API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

    headers = {
        "x-app-id": os.environ["NUTRITIONIX_APPID"],
        "x-app-key": os.environ["NUTRITIONIX_APPKEY"],
        # "x-remote-user-id": 0,
    }

    user_input = input("Tell me which exercises you did: ")

    body = {
        "query": user_input,
        "gender": "male",
        "weight_kg": 65,
        "height_cm": 163,
        "age": 27,
    }

    r = requests.post(url=API_URL, json=body, headers=headers)
    print(r.text)
    return r.json()["exercises"]


def write_to_sheet(data: List[Dict]):
    API_URL = (
        "https://api.sheety.co/fc3b6272633e38c647f286f2efc491f4/myWorkouts/workouts"
    )

    headers = {
        "Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}",
    }

    now = dt.now()

    for e in data:
        body = {
            "workout": {
                "date": now.strftime(r"%d/%m/%Y"),
                "time": now.strftime(r"%H:%M:%S"),
                "exercise": e["name"].title(),
                "duration": e["duration_min"],
                "calories": e["nf_calories"],
            }
        }
        r = requests.post(url=API_URL, json=body, headers=headers)
        r.raise_for_status()
        print(r.text)


write_to_sheet(get_exercise_data())
