from account_data_retriever import AccountDataRetriever
import plotly.graph_objects as go
from templates import constants
from datetime import datetime
import os


class WebpageDataRefresher(AccountDataRetriever):
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
      converted_equity_values.append(round(equity - float(self.account.cash), 2))

    return converted_equity_values


  def __get_equities_and_times(self):
    portfolio_object = self.api.get_portfolio_history(date_start=None, date_end=None, period="1D", timeframe="5Min", extended_hours=True)
    equity_data = self.__convert_equities_from_api(portfolio_object)
    time_data = self.__convert_timestamps_from_api(portfolio_object)
    return tuple((equity_data, time_data))


  def create_plot_html(self) -> str:
    equity_data, time_data = self.__get_equities_and_times()
    fig = go.Figure([go.Scatter(x=time_data, y=equity_data, line=dict(color="yellow"))])
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
          <h1 id="top" class="num">${self.get_stock_equity()}</h1>
          <h2 class="color num">{self.get_account_daily_change()} ({self.get_account_percent_change()}%)</h2>
          {graph_div}
          <div class="buyingpower">
              <p class="buy">Buying Power</p>
              <p class="buy2 num">${self.get_buying_power()}</p>
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
