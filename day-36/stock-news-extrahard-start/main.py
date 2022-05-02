import os
from datetime import datetime as dt
from typing import List

import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_2_most_recent_dates(dates: List[dt]) -> List[dt]:
    sorted_dates = sorted(dates, reverse=True)
    return sorted_dates[:2]


# Check diff between closing prices of 2 latest days and return true if it is above 5%
def get_price_change() -> float:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": os.environ["ALPHA_VANTAGE_API_KEY"],
    }
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    daily_data = response.json()["Time Series (Daily)"]

    recent_dates = get_2_most_recent_dates(
        [dt.strptime(d, r"%Y-%m-%d") for d in daily_data.keys()]
    )

    p_latest = float(daily_data[recent_dates[0].strftime(r"%Y-%m-%d")]["4. close"])
    p_2nd_latest = float(daily_data[recent_dates[1].strftime(r"%Y-%m-%d")]["4. close"])
    return (p_latest - p_2nd_latest) * 100 / p_2nd_latest


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_latest_3_news() -> List:
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": os.environ["NEWS_API_KEY"],
        "q": COMPANY_NAME,
        "searchIn": "title",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 3,
        "page": 1,
    }
    response = requests.get(url=url, params=params)
    response.raise_for_status()

    articles = response.json()["articles"]
    return articles


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
def send_sms(price_change: float, articles: List):
    account_sid = os.getenv("TWILIO_ACC")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_number = "+16165801062"
    to_number = "+84969272995"

    client = Client(account_sid, auth_token)

    change_text = f"{STOCK}: {'🔺' if price_change > 0 else '🔻'}{abs(price_change):.1f}%"

    for article in articles:
        msg = client.messages.create(
            to=to_number,
            from_=from_number,
            body=f"{change_text}\nHeadline: {article['title']}\nBrief: {article['description']}",
        )
        print(msg.sid)


price_change = get_price_change()
print(f"Price change is {price_change:.2f}%.")
if abs(price_change) >= 5:
    print(f" Sending SMS")
    send_sms(price_change=price_change, articles=get_latest_3_news())
