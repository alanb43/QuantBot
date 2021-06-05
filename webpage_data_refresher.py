from alpaca_trade_api.rest import Positions
from trader import *
import time

class Stock:
  '''
  
  Stock object to store key information regarding a stock for the purpose of
  supplying QuantBot.io with correct info. Used with WebpageDataRefresher. 

  '''
  def __init__(self, symbol, qty, current_price, lastday_price, market_value, 
            unrealized_intraday_pl, unrealized_intraday_plpc) -> None:
    self.symbol = symbol
    self.qty = qty
    self.current_price = current_price
    self.lastday_price = lastday_price
    self.market_value = market_value
    self.intraday_pl = unrealized_intraday_pl
    self.intraday_plpc = unrealized_intraday_plpc


  def __str__(self):
    ''' Returns a paragraph blurb listing all of the data the object holds. '''
    string = f'''{self.symbol}\nQty: {self.qty}\nCurrent Price: {self.current_price}\n'''
    string += f'''Yesterday's Close: {self.lastday_price}\nMarket Value: {self.market_value}\n'''
    string += f'''Today's P/L: {self.intraday_pl}\nToday's P/L % Change: {self.intraday_plpc}\n'''
    return string
    

  def __lt__(self, other_stock):
    ''' Overloaded less than operator, for alphabetical sorting of stocks based on symbol '''
    return self.symbol < other_stock.symbol


class WebpageDataRefresher:
  '''

  Webpage Data Refresher tool to supply QuantBot.io with latest information regarding
  equities, positions, profits & losses, and more. Generally returns tuples containing
  the float for a particular case and it's formatted string.

  NOTE: functionality for sidebar refreshing needs to be added
  NOTE: this class can / maybe will be used in conjunction with a server that runs it
        to update the site periodically

  '''
  def __init__(self) -> None:
    self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    self.account = self.api.get_account()
    self.positions = self.api.list_positions()


  def __number_float_to_string(self, float) -> str:
    return f'{float :,.2f}'


  def __format_dollars_to_string(self, float) -> str:
    string = self.__number_float_to_string(float)
    if str(float)[0] == '-':
      return "-$" + string[1:]
    return "+$" + string


  def __format_percentage_to_string(self, percentage) -> str:
    if percentage >= 0:
      return '+' + self.__number_float_to_string(percentage)
    return '-' + self.__number_float_to_string(percentage)


  def get_equity(self) -> tuple((float, str)):
    return tuple((float(self.account.equity), self.__number_float_to_string(float(self.account.equity))))


  def get_buying_power(self) -> tuple((float, str)):
    buying_power = float(self.account.buying_power)
    return tuple((buying_power, self.__number_float_to_string(buying_power)))  


  def __get_account_positions(self) -> list:
    positions = self.api.list_positions()
    positions_array = []
    for position in positions:
      symbol = position.symbol
      qty = position.qty
      price = position.current_price
      lastday_price = position.lastday_price
      market_val = position.market_value
      intraday_pl = position.unrealized_intraday_pl
      intraday_plpc = position.unrealized_intraday_plpc
      positions_array.append(Stock(symbol, qty, price, lastday_price, market_val, intraday_pl, intraday_plpc))
    
    return positions_array


  def get_account_daily_change(self) -> tuple((float, str)):
    daily_change = 0
    positions = self.__get_account_positions()
    for position in positions:
      daily_change += float(position.intraday_pl)

    return tuple((daily_change, self.__format_dollars_to_string(daily_change)))


  def get_account_percent_change(self) -> tuple((float, str)):
    percent_change = 0
    positions = self.__get_account_positions()
    equity = (self.get_equity())[0]
    for position in positions:
      percent_change += float( position.intraday_plpc ) * ( ( float(position.market_value) * float(position.qty) ) / equity )

    return tuple((percent_change, self.__format_percentage_to_string(percent_change)))


  def print_stock_price_alphabetical(self):
    ''' for debugging, so you can see what your handling '''
    positions = self.__get_account_positions()
    for position in sorted(positions):
      print(position)


WDR = WebpageDataRefresher()
WDR.print_stock_price_alphabetical()


# AAPL_VALUE = float(aapl_position.current_price)
# AAPL_VALUE = "{:,.2f}".format(AAPL_VALUE)
# if AAPL_VALUE[0] == "-":
#   AAPL_VALUE = "-$" + AAPL_VALUE[1:]
# else:
#   AAPL_VALUE = "$" + AAPL_VALUE

# AAPL_PERCHANGE = ((float(aapl_position.current_price) - float(aapl_position.lastday_price)) / float(aapl_position.lastday_price)) * 100
# AAPL_PERCHANGE = "{:.2f}".format(AAPL_PERCHANGE)
# if AAPL_PERCHANGE[0] == "-":
#   AAPL_COLOR = "red"
# elif float(AAPL_PERCHANGE) > 0:
#   AAPL_COLOR = "green"
# else:
#   AAPL_COLOR = "white"

# TSLA_VALUE = float(tsla_position.current_price)
# TSLA_VALUE = "{:,.2f}".format(TSLA_VALUE)
# if TSLA_VALUE[0] == "-":
#     TSLA_VALUE = "-$" + TSLA_VALUE[1:]
# else:
#     TSLA_VALUE = "$" + TSLA_VALUE

# TSLA_PERCHANGE = ((float(tsla_position.current_price) - float(tsla_position.lastday_price)) / float(tsla_position.lastday_price)) * 100
# TSLA_PERCHANGE = "{:.2f}".format(TSLA_PERCHANGE)
# if TSLA_PERCHANGE[0] == "-":
#   TSLA_COLOR = "red"
# elif float(TSLA_PERCHANGE) > 0:
#   TSLA_COLOR = "green"
# else:
#   TSLA_COLOR = "white"

# GOOGL_VALUE = float(googl_position.current_price)
# GOOGL_VALUE = "{:,.2f}".format(GOOGL_VALUE)
# if GOOGL_VALUE[0] == "-":
#     GOOGL_VALUE = "-$" + GOOGL_VALUE[1:]
# else:
#     GOOGL_VALUE = "$" + GOOGL_VALUE

# GOOGL_PERCHANGE = ((float(googl_position.current_price) - float(googl_position.lastday_price)) / float(googl_position.lastday_price)) * 100
# GOOGL_PERCHANGE = "{:.2f}".format(GOOGL_PERCHANGE)
# if GOOGL_PERCHANGE[0] == "-":
#   GOOGL_COLOR = "red"
# elif float(GOOGL_PERCHANGE) > 0:
#   GOOGL_COLOR = "green"
# else:
#   GOOGL_COLOR = "white"

# html_content = f"""<!DOCTYPE html>
# <head>
#   <link rel="stylesheet" href="styles.css">
#   <link rel="preconnect" href="https://fonts.gstatic.com">
#   <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
#   <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
#   <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
#   <title>QuantBot</title>
#   <link rel="shortcut icon" href="favicon.ico">
# </head>
# <body>
#   <div class="nav-bar">
#     <a href="#top">
#     <video disableRemotePlayback autoplay muted loop id="myVideo">
#       <source src="logo.mp4" type="video/mp4">
#     </video>
#   </a>
#     <ul class="nav-buttons">
#       <li class="button color"><a style = "text-decoration: none; color: inherit" href="#top">Portfolio</a></li>
#       <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
#       <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
#     </ul>
#   </div>
#   <div class="side-bar">
#     <ul class="shares">
#       <li class="share">
#         <ul class="share-details">
#           <li>AAPL</li>
#           <li class="value"><p>{AAPL_VALUE}</p><p class="per" style="color: {AAPL_COLOR}">{AAPL_PERCHANGE}%</p></li>
#         </ul>
#       </li>
#       <li class="share">
#         <ul class="share-details">
#           <li>TSLA</li>
#           <li class="value"><p>{TSLA_VALUE}</p><p class="per" style="color: {TSLA_COLOR}">{TSLA_PERCHANGE}%</p></li>
#         </ul>
#       </li>
#       <li class="share">
#         <ul class="share-details">
#           <li>GOOGL</li>
#           <li class="value"><p>{GOOGL_VALUE}</p><p class="per" style="color: {GOOGL_COLOR}">{GOOGL_PERCHANGE}%</p></li>
#         </ul>
#       </li>
#     </ul>
#   </div>
#   <div class="body">
#     <h1 id="top">${account_equity_str}</h1>
#     <h2 class="color">{daily_change} ({percent_change_str}%) Today</h2>
#     <img src="fakegraph.png" alt="graph" class="fakegraph">
#     <div class="buyingpower">
#         <p class="buy">Buying Power</p>
#         <p class="buy2">${buying_power}</p>
#     </div>
#     <div class="summary">
#       <p class="color">What is Quantbot?</p>
#       <p class="des">Quantbot is a Python Bot that utilizes a combination of machine learning, time analysis, and sentiment analysis to automatically buy and sell stocks. The bot uses a web scraper that periodically checks for new articles regarding a company and analyzes the content in the article. If the bot deems the article particularly positive or negative for that company, the bot will either buy or sell the shares we have.</p>
#     </div>
#     <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
#     <div class="news">
#       <ul class="news-list">
#         <li class="article">
#           <ul class="inner-article">
#             <li>
#               <img src="a.png" alt="graph" class="article-img">
#             </li>
#             <li class="article-words">
#               <p class="article-summary color">This article led to the bot buying 10 shares of AAPL.</p>
#               <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
#             </li>
#           </ul>
#         </li>
#         <li class="article">
#           <ul class="inner-article">
#             <li>
#               <img src="a.png" alt="graph" class="article-img">
#             </li>
#             <li class="article-words">
#               <p class="article-summary color">This article led to the bot selling 20 shares of GOOGL.</p>
#               <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
#             </li>
#           </ul>
#         </li>
#         <li class="article">
#           <ul class="inner-article">
#             <li>
#               <img src="a.png" alt="graph" class="article-img">
#             </li>
#             <li class="article-words">
#               <p class="article-summary color">This article led to the bot buying 15 shares of TSLA.</p>
#               <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
#             </li>
#           </ul>
#         </li>
#       </ul>
#     </div>
#     <div class="contact color" id="contact">
#       <h3 style="margin-bottom: -10px; font-size: 18px;">Contact Us</h3>
#       <p style="margin-bottom: -10px; font-size: 15px;">Josh Cunningham || jcun@umich.edu || LinkedIn</p>
#       <p style="font-size: 15px">Alan Bergsneider || bera@umich.edu || LinkedIn</p>
#     </div>
#   </div>

# </body>"""

# with open("webpage/index.html", "w") as html_file:
#     html_file.write(html_content)

# time.sleep(1)