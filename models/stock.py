from dataclasses import dataclass

@dataclass
class Stock:
  '''
  Stock object to store key information regarding a stock for the purpose of
  supplying QuantBot.io with correct info. Used with WebpageDataRefresher. 
  '''
  
  symbol: str
  qty: int
  current_price: float
  lastday_price: float
  market_value: float # might need to change to qty * current_price
  intraday_pl: float
  intraday_plpc: float
  change_today: float
  pl: float
  plpc: float
  cost: float
  abs_intraday_plpc: float


  def __lt__(self, other_stock):
    ''' Overloaded less than operator, for alphabetical sorting of stocks based on symbol '''
    return self.symbol < other_stock.symbol

  def __gt__(self, other_stock):

    return abs(self.plpc) > abs(other_stock.plpc)
