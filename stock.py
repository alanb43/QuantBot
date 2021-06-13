class Stock:
  '''
  Stock object to store key information regarding a stock for the purpose of
  supplying QuantBot.io with correct info. Used with WebpageDataRefresher. 
  '''
  def __init__(self, symbol, qty, current_price, lastday_price, market_value, 
            unrealized_intraday_pl, unrealized_intraday_plpc, change_today, pl,
            plpc, cost) -> None:
    self.symbol = symbol
    self.qty = qty
    self.current_price = current_price
    self.lastday_price = lastday_price
    self.market_value = market_value
    self.intraday_pl = unrealized_intraday_pl
    self.intraday_plpc = unrealized_intraday_plpc
    self.market_value = float(current_price) * float(qty)
    self.change_today = change_today
    self.pl = pl
    self.plpc = plpc
    self.cost = cost


  def __str__(self):
    ''' Returns a paragraph blurb listing all of the data the object holds. '''
    string = f'''{self.symbol}\nQty: {self.qty}\nCurrent Price: {self.current_price}\n'''
    string += f'''Yesterday's Close: {self.lastday_price}\nMarket Value: {self.market_value}\n'''
    string += f'''Today's P/L: {self.intraday_pl}\nToday's P/L % Change: {self.intraday_plpc}\n'''
    string += f"Market value: {self.market_value}\nOverall PL: {self.pl}\nOverall PLPC: {self.plpc}\n"
    string += f'''Avg cost per share: {self.cost}\n'''
    return string


  def __lt__(self, other_stock):
    ''' Overloaded less than operator, for alphabetical sorting of stocks based on symbol '''
    return self.symbol < other_stock.symbol