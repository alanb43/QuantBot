from alpaca_trade_api.rest import Positions
from trader import *
import time
import matplotlib.pyplot as plt # side-stepping mpl backend
import numpy as np
import plotly.graph_objects as go
from templates import constants
from datetime import date, datetime
import os

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
    self.market_value = current_price * qty



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
  NOTE: initializing an instance connects us to the api and sets class up with account
        and positions info
  NOTE: functionality for sidebar refreshing needs to be added
  NOTE: this class can / maybe will be used in conjunction with a server that runs it
        to update the site periodically
  '''
  def __init__(self) -> None:
    self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    self.account = self.api.get_account()
    self.__api_positions = self.api.list_positions()
    self.positions = self.__get_account_positions(self.__api_positions)

  def __number_float_to_string(self, float) -> str:
    ''' Turns a float into a formatted string '''
    return f'{float :,.2f}'


  def __format_dollars_to_string(self, float) -> str:
    ''' Formats a dollar string with dollar signs and direction '''
    string = self.__number_float_to_string(float)
    if str(float)[0] == '-':
      return "-$" + string[1:]
    return "+$" + string


  def __format_percentage_to_string(self, percentage) -> str:
    ''' Formats a percentage string with direction '''
    if percentage >= 0:
      return '+' + self.__number_float_to_string(percentage)
    return self.__number_float_to_string(percentage)[0] + ' ' + self.__number_float_to_string(percentage)[1:]


  def get_stock_equity(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for account equity and
    a formatted string of this value.
    '''
    equity = 0
    for position in self.positions:
      equity += position.market_value
    
    return tuple((float(equity), self.__number_float_to_string(float(equity))))


  def get_buying_power(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for buying power and a
    formatted string of this value.
    '''
    buying_power = float(self.account.buying_power) - 1500000
    return tuple((buying_power, self.__number_float_to_string(buying_power)))  


  def __get_account_positions(self, api_positions) -> list:
    '''
    Goes through positions received from Alpaca, initializes Stock objects with
    relevant info, adds them to an array which is eventually returned.
    '''
    stock_array = []
    for position in api_positions:
      stock_array.append(
        Stock(
          position.symbol, position.qty, position.current_price, 
          position.lastday_price, position.market_value, 
          position.unrealized_intraday_pl, position.unrealized_intraday_plpc
        )
      )
    return stock_array


  def get_account_daily_change(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for the account's daily change 
    and a formatted string of this value.
    '''
    daily_change = 0
    for position in self.positions:
      daily_change += float(position.intraday_pl)

    return tuple((daily_change, self.__format_dollars_to_string(daily_change)))


  def get_lastday_equity(self) -> tuple((float, str)):
    
    lastday_equity = 0
    for position in self.__get_account_positions():
      lastday_equity += ( float(position.lastday_price) * float(position.qty) ) 
    return tuple((lastday_equity, self.__number_float_to_string(lastday_equity))) 


  def get_account_percent_change(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for the account's daily percent 
    change and a formatted string of this value.
    '''
    percent_change = 0
    equity = self.get_stock_equity()[0]
    for position in self.positions:
      percent_change += float( position.intraday_plpc ) * ( ( float(position.market_value) * float(position.qty) ) / equity )

    return tuple((percent_change, self.__format_percentage_to_string(percent_change)))

  
  def print_stock_price_alphabetical(self):
    ''' for debugging, so you can see what your handling '''
    for position in sorted(self.positions):
      print(position)


  def get_position_colors(self) -> dict:
    colors = {}
    for x in range(len(self.positions)):
      if float(self.positions[x].intraday_plpc) >= 0:
        colors[self.positions[x].symbol] = "green"
      else:
        colors[self.positions[x].symbol] = "red"
    return colors


  def __convert_timestamps_from_api(self, portfolio_object) -> list:
    timestamps = portfolio_object.timestamp
    time_array = []
    for stamp in timestamps:
      dt = datetime.fromtimestamp(stamp)
      time = str(dt)[11:-3]
      time_array.append(time)
    
    return time_array
  

  def __convert_equities_from_api(self, portfolio_object) -> list:
    converted_equity_values = []
    for equity in portfolio_object.equity:
      converted_equity_values.append('$' + self.__number_float_to_string(equity - 500000))
    
    return converted_equity_values


  def __get_equities_and_times(self):
    portfolio_object = self.api.get_portfolio_history(date_start=None, date_end=None, period="1D", timeframe="5Min", extended_hours=None)
    equity_data = self.__convert_equities_from_api(portfolio_object)
    time_data = self.__convert_timestamps_from_api(portfolio_object)
    return tuple((equity_data, time_data))


  def create_plot_html(self) -> str:
    equity_data, time_data = self.__get_equities_and_times()
    fig = go.Figure([go.Scatter(x=time_data, y=equity_data,line=dict(color="yellow"))])
    fig.layout.xaxis.color = 'white'
    fig.layout.yaxis.visible = False
    fig.layout.paper_bgcolor = 'rgba(0, 0, 0, 0)'
    fig.layout.plot_bgcolor='black'
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout( xaxis = dict(dtick = 12) )
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    with open('./templates/graph.html', 'w') as f:
      f.write(fig.to_html(include_plotlyjs='cdn', default_width="90%", config={"displayModeBar": False}))
    with open('./templates/graph.html', 'r') as graph:
      graph.readline()
      graph.readline()
      graph.readline()
      graph_div = graph.readline()
      graph_div += graph.readline()
    os.remove('./templates/graph.html')
    return graph_div
  

  def create_site_html(self) -> str:
    graph_div = self.create_plot_html()
    with open("templates/index.html", "w") as html_file:
      html_top = constants.TOP_OF_PAGE
      html_file.write(html_top)
      for x in range(len(self.positions)):
        price = "{:,.2f}".format(float(self.positions[x].current_price))
        percent = self.__format_percentage_to_string(float(self.positions[x].intraday_plpc) * 100)
        html_content = f"""        
            <li class="share">
              <ul class="share-details">
                <li ><p style="margin-bottom: -10px; top: -40%;">{self.positions[x].symbol}</p><p class="quantity">{self.positions[x].qty} Shares</p></li>
                <li class="value"><p class="num">${price}</p><p class="per num" style="color: {self.get_position_colors()[self.positions[x].symbol]}; font-weight: bold">{percent}%</p></li>
              </ul>
              
            </li> """
        html_file.write(html_content)

      html_content = f"""
          </ul>
        </div>
        <div class="body">
          <h1 id="top" class="num">${self.get_stock_equity()[1]}</h1>
          <h2 class="color num">{self.get_account_daily_change()[1]} ({self.get_account_percent_change()[1]}%)</h2>
          {graph_div}
          <div class="buyingpower">
              <p class="buy">Buying Power</p>
              <p class="buy2 num">${self.get_buying_power()[1]}</p>
          </div>
          <div class="summary">
            <p class="color" style="font-weight: bold">What is Quantbot?</p>
            <p class="des">QuantBot is a completely automated bot that makes use of artificial intelligence to trade 
              the stock market for its founders, <a class="us" href="https://bergsneider.dev" target="_blank">Alan</a> and 
              <a class="us" href="https://joshcunningham.net" target="_blank">Josh</a>. We've programmed the bot using Python 
              to scrape the web to find data it desires regarding different assets, perform machine learning (both time series 
              and sentiment analyses with price and news data respectively), and finally decide to buy/sell using the Alpaca 
              API and brokerage based on the conclusions of the analyses when compared against each other. This project is 
              being completed over Summer 2021 outside of our professional endeavours, and we are learning all of these concepts
              (web scraping, time series analysis, sentiment analysis / Natural Language Processing, financial reporting, etc) on
              our own from scratch. 
            </p>
          </div>
          <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
          <div class="news">
            <ul class="news-list">
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="resources/a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot buying 10 shares of AAPL.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="resources/a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot selling 20 shares of GOOGL.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="resources/a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot buying 15 shares of TSLA.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        """
      html_file.write(html_content)
      html_file.write(constants.BOTTOM_OF_PAGE)

WDR = WebpageDataRefresher()
WDR.create_site_html()
# WDR.print_stock_price_alphabetical()
