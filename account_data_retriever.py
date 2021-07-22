from config import *
from models.stock import Stock
import operator

class AccountDataRetriever:
  '''
  This class allows for easy access to relevent account information for debugging, 
  updating the webpage, etc.
  
  NOTE: initializing an instance connects us to the api and sets class up with account
        and positions info

  '''
  def __init__(self) -> None:
    self.api = API
    self.account = self.api.get_account()
    self.positions = self.__get_account_positions()
    self.plpc_sorted_holdings = sorted(self.positions, key=operator.attrgetter('abs_intraday_plpc'), reverse=True)
  

  def __get_account_positions(self) -> list:
    '''
    Goes through positions received from Alpaca, initializes Stock objects with
    relevant info, adds them to an array which is eventually returned.
    '''
    positions = []
    for position in self.api.list_positions():
      positions.append(
        Stock(
            position.symbol, int(position.qty), float(position.current_price), 
            float(position.lastday_price), float(position.market_value), 
            float(position.unrealized_intraday_pl), float(position.unrealized_intraday_plpc),
            float(position.change_today), float(position.unrealized_pl), 
            float(position.unrealized_plpc), float(position.avg_entry_price), 
            abs(float(position.market_value))
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
    yesterday_equity = self.get_stock_equity() - self.get_account_daily_change()
    return ( ( self.get_stock_equity() - yesterday_equity ) / yesterday_equity ) * 100


  def get_position_colors(self) -> dict:
    '''
    Returns a dictionary mapping strings of stock symbols to a string, either
    'green' or 'red' based on if the stock is up / down on the day.
    '''
    colors = {}
    for position in self.positions:
      if position.intraday_pl >= 0:
        colors[position.symbol] = "green"
      else:
        colors[position.symbol] = "red"
    
    return colors

  
  def print_stock_price_alphabetical(self):
    ''' for debugging, so you can see what you're handling '''
    for position in sorted(self.positions):
      print(position)
