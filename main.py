import requests
from pprint import pprint
import datetime as dt
import html
import time
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = 'YOUR_TWILIO_ACCOUNT_SSID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'

def calculate(new_value, old_value):
    percentage_inc_or_dec = ((new_value["4. close"] - old_value["4. close"]) / new_value["4. close"]) * 100
    return float(percentage_inc_or_dec)

parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "interval" : "1min",
    "appikey": "YOUR_alpha_vantage_API_key"
}

stock_url = "https://www.alphavantage.co/query"
response = requests.get(url=stock_url, params=parameters)
response.raise_for_status()

now = dt.datetime.now()
current_date = now.date()
yesterday, yesterday_back = {current_date - dt.timedelta(days=1), current_date - dt.timedelta(days=2)}

data = response.json()["Time Series (Daily)"]
yesterday_stock, yesterday_back_stock =  [data[str(yesterday)], data[str(yesterday_back)]]

stock_percentage = calculate(yesterday_stock, yesterday_back_stock)


news_url = "https://newsapi.org/v2/everything"

news_params = {
    "q": COMPANY_NAME,
    "language": "en",
    "apiKey": "your_newsapi_apikey",
    "from": yesterday_back,
    "to": yesterday,
    "sortBy": "relevancy",
    "pageSize": 3,
}

res = requests.get(url=news_url, params=news_params)
res.raise_for_status()

news_data = res.json()
articles = news_data["articles"]


stock_sign = ""
if stock_percentage > 0:
    stock_sign = f"TSLA: 🔺{round(stock_percentage, 2)}%"
else:
    stock_sign = f"TSLA: 🔻{round(stock_percentage, 2)}%"


client = Client(account_sid, auth_token)
for article in articles:
    msg_text = str(html.unescape(f"{stock_sign}\nHeadline: {html.unescape(article["title"])}\nBrief: {html.unescape(article["description"])}"))
    print(msg_text)
    message = client.messages.create(
        from_='YOUR_PHONE_NUMBER_GIVEN_TO_YOU_ON_TWILIO',
        body=msg_text,
        to='YOUR_VERIFIED_PHONE_NUMBER'
    )
    time.sleep(3)








