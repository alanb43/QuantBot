import alpaca_trade_api as tradeapi
import requests
from config import *

url = "https://paper-api.alpaca.markets"

r = requests.get(url)
print(r.content)

api = tradeapi.REST(API_KEY, SECRET_KEY, url, api_version='v2')

account = api.get_account()
print(account)

