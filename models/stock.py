class Stock:
  '''
  Stock object to store key information regarding a stock for the purpose of
  supplying QuantBot.io with correct info. Used with WebpageDataRefresher. 
  '''
  def __init__(self, stock_info) -> None:
    self.symbol = stock_info[0]
    self.qty = stock_info[1]
    self.current_price = stock_info[2]
    self.lastday_price = stock_info[3]
    self.market_value = stock_info[4]
    self.intraday_pl = stock_info[5]
    self.intraday_plpc = stock_info[6]
    self.market_value = float(stock_info[2]) * float(stock_info[1])
    self.change_today = stock_info[7]
    self.pl = stock_info[8]
    self.plpc = stock_info[9]
    self.cost = stock_info[10]


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