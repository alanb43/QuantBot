import alpaca_trade_api as tradeapi
from config import *
from models.stock import Stock

class AccountDataRetriever:


  def __init__(self) -> None:
    self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    self.account = self.api.get_account()
    self.positions = self.__get_account_positions()
  

  def __get_account_positions(self) -> list:
    '''
    Goes through positions received from Alpaca, initializes Stock objects with
    relevant info, adds them to an array which is eventually returned.
    '''
    positions = []
    for position in self.api.list_positions():
      positions.append(
        Stock(
          [
            position.symbol, float(position.qty), float(position.current_price), 
            float(position.lastday_price), float(position.market_value), 
            float(position.unrealized_intraday_pl), float(position.unrealized_intraday_plpc),
            float(position.change_today), float(position.unrealized_pl), 
            float(position.unrealized_plpc), float(position.avg_entry_price)
          ]
        )
      )

    return positions


  def get_stock_equity(self) -> float:
    '''
    Returns a tuple containing the float value for account equity and
    a formatted string of this value.
    '''
    equity = 0
    for position in self.positions:
      equity += position.market_value
    
    return equity


  def get_buying_power(self) -> float:
    '''
    Returns a tuple containing the float value for buying power and a
    formatted string of this value.
    '''
    buying_power = float(self.account.cash)
    return buying_power


  def get_account_daily_change(self) -> float:
    '''
    Returns a tuple containing the float value for the account's daily change 
    and a formatted string of this value.
    '''
    daily_change = 0
    for position in self.positions:
      daily_change += position.current_price - position.lastday_price

    return daily_change


  def get_account_percent_change(self) -> float:
    '''
    Returns a tuple containing the float value for the account's daily percent 
    change and a formatted string of this value.
    '''
    percent_change = 0
    for position in self.positions:
      percent_change += ( position.change_today * ( position.market_value / self.get_stock_equity() ) )

    return percent_change


  def get_position_colors(self) -> dict:
    colors = {}
    for position in self.positions:
      if position.intraday_pl >= 0:
        colors[position.symbol] = "green"
      else:
        colors[position.symbol] = "red"
    
    return colors

  
  def print_stock_price_alphabetical(self):
    ''' for debugging, so you can see what your handling '''
    for position in sorted(self.positions):
      print(position)
