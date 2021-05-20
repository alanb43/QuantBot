from typing import OrderedDict
import requests, json
import alpaca_trade_api as tradeapi
from config import *

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = f"{BASE_URL}/v2/account"
ORDERS_URL = f"{BASE_URL}/v2/orders"
HEADERS = {"APCA-API-KEY-ID":API_KEY, "APCA-API-SECRET-KEY":SECRET_KEY}

def get_account():
  r = requests.get(ACCOUNT_URL, headers=HEADERS)
  print(r.content)
  return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
  data = {
    "symbol": symbol,
    "qty": qty,
    "side": side,
    "type": type,
    "time_in_force":time_in_force
  }

  r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
  return json.loads(r.content)


def get_orders():
  r = requests.get(ORDERS_URL, headers=HEADERS)
  return json.loads(r.content)

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

account = api.get_account()
print(account.status)


# Stock Symbol, quantity, buy or sell, market (unless you want to do 
# limit buy/sell), and day unless you want before / after hours trading
purchase_response = create_order("AAPL", 50, "buy", "market", "day")
print(purchase_response)