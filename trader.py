import requests, json
import alpaca_trade_api as tradeapi
from config import *

class Trader:
  '''

  Trading tool for the Alpaca API, able to create JSON formatted objects, 
  use these objects to place orders, and cancel orders.

  1. Debug functions
  2. JSON Object making functions
  3. Placing and Cancelling Orders

  NOTE: Create an instance : T = Trader(), use instance to call functions.

  '''

  def __init__(self) -> None:
    __api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    return

  ''' 1. Debug functions '''

  def get_account(self):
    '''
    EFFECTS: loads account status
    NOTE: really shouldn't be used unless troubleshooting
    '''
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


  def get_orders(self):
    '''
    EFFECTS: prints all orders placed in a dictionary.
    NOTE: really shouldn't be used unless troubleshooting
    '''
    r = requests.get(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)

  ''' 2. JSON Object making functions '''

  def __add_bracket_order_data(self, data, profit_limit, stop_loss):
    '''
    NOTE: ONLY USE WITHIN create_market_order_data
    REQUIRES: dictionary from create_market_order_data, ints representing profit
              limit and stop loss
    MODIFIES: data
    EFFECTS:  returns dictionary representing JSON object for a bracket order
    '''
    data["order_class"] = "bracket"
    data["take_profit"] = {"limit_price": profit_limit}
    data["stop_loss"] = {"stop_price" : stop_loss}
    return data


  def create_market_order_data(self, ticker, qty, side, order_type, time_in_force, bracket = False, profit_limit = -1, stop_loss = -1):
    '''
    REQUIRES: string representing ticker, int representing qty, string representing
              side (buy / sell), string representing order type (market, etc), string
              representing time in force (day, gtc, etc). IF DOING LIMIT ORDER: True
              for bracket, int for profit limit, int for stop loss.
    EFFECTS:  returns a dictionary formatted for the POST operation
    '''
    data = {
      "symbol": ticker,
      "qty": qty,
      "side": side,
      "type": order_type,
      "time_in_force":time_in_force
    }
    if bracket:
      data = self.__add_bracket_order_data(data, profit_limit, stop_loss)
    return data

  ''' 3. Placing / Cancelling Orders '''

  def place_order(self, data):
    '''
    REQUIRES: properly formatted dictionary representing JSON order object.
    EFFECTS:  posts the order to the Alpaca API, returns API message.
    '''
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


  def cancel_order(self, order_id):
    '''
    REQUIRES: valid order_id (first value in json object returned from place_order)
    EFFECTS:  cancels an order placed (if not already executed), returns message
    '''
    r = requests.delete(ORDERS_URL + f'/{order_id}', headers=HEADERS) 
    return json.loads(r.content)
  

  def cancel_all_orders(self):
    '''
    EFFECTS: cancels all orders (if possible)
    '''
    r = requests.delete(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)
