from typing import OrderedDict
import requests, json
import alpaca_trade_api as tradeapi
from config import *

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = f"{BASE_URL}/v2/account"
ORDERS_URL = f"{BASE_URL}/v2/orders"
HEADERS = {"APCA-API-KEY-ID":API_KEY, "APCA-API-SECRET-KEY":SECRET_KEY}

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
account = api.get_account()

def get_account():
  r = requests.get(ACCOUNT_URL, headers=HEADERS)
  return json.loads(r.content)

# Stock Symbol, quantity, buy or sell, market (unless you want to do 
# limit buy/sell), and day unless you want before / after hours trading

def create_market_order_data(symbol, qty, side, type, time_in_force):
  data = {
    "symbol": symbol,
    "qty": qty,
    "side": side,
    "type": type,
    "time_in_force":time_in_force
  }
  return data

def create_bracket_order_data(symbol, qty, side, type, time_in_force, profit_limit, stop_loss):
  data = {
    "symbol": symbol,
    "qty": qty,
    "side": side,
    "type": type,
    "time_in_force": time_in_force,
    "order_class": "bracket",
    "take_profit": {
      "limit_price": profit_limit
    },
    "stop_loss": {
      "stop-price": stop_loss
    }
  }
  return data

def place_order(data):
  r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
  print(json.loads(r.content))
  return json.loads(r.content)


def get_orders():
  r = requests.get(ORDERS_URL, headers=HEADERS)
  return json.loads(r.content)

my_order = create_market_order_data("AAPL", 10, "buy", "market", "day")
place_order(my_order)
