import alpaca_trade_api as tradeapi
from config import *

class AccountDataRetriever:


  def __init__(self) -> None:
    self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    self.account = self.api.get_account()
    self.__api_positions = self.api.list_positions()
    self.positions = self.__get_account_positions(self.__api_positions)
  

  def get_stock_equity(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for account equity and
    a formatted string of this value.
    '''
    equity = 0
    for position in self.positions:
      equity += position.market_value
    
    return tuple((float(equity), self.__number_float_to_string(float(equity))))