from account_data_retriever import AccountDataRetriever
import plotly.graph_objects as go
from models import webpage
from datetime import datetime
import os

class WebpageDataRefresher(AccountDataRetriever):
  '''
  Webpage Data Refresher tool to supply QuantBot.io with latest information regarding
  equities, positions, profits & losses, and more. 
  
  When initialized, AccountDataRetriever's __init__ is used to connect us to the API

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


  def __convert_timestamps_from_api(self, portfolio_object):
    ''' Converts timestamp objects to human readable times '''
    timestamps = portfolio_object.timestamp
    time_array = []
    for stamp in timestamps:
      dt = datetime.fromtimestamp(stamp)
      time = str(dt)[11:-3]
      if int(time[0:2]) > 12:
        time = str ( int(time[0:2]) % 12 ) + time[2:] + "P"
      elif int(time[0:2]) == 12:
        time += "P"
      else:
        time = str ( int(time[0:2])) + time[2:] + "A"
      time_array.append(time)
    
    return time_array
  

  def __convert_equities_from_api(self, portfolio_object):
    ''' Converts equities to appropriate values for graph '''
    converted_equity_values = []
    for equity in portfolio_object.equity:
      if equity:
        converted_equity_values.append(round(equity - float(self.account.cash), 2))
    return converted_equity_values


  def __get_equities_and_times(self):
    ''' Calls other functions to get equity data and time data for graph axes '''
    portfolio_object = self.api.get_portfolio_history(date_start=None, date_end=None, period="1D", timeframe="5Min", extended_hours=True)
    equity_data = self.__convert_equities_from_api(portfolio_object)
    time_data = self.__convert_timestamps_from_api(portfolio_object)
    return tuple((equity_data, time_data))

  
  def format_sidebar_content(self, position):
    ''' Generates formatted content for an individual holding in the sidebar '''
    position_values = []
    position_values.append(position.symbol)
    position_values.append(position.qty)
    position_values.append("{:,.2f}".format(position.current_price))
    position_values.append(self.get_position_colors()[position.symbol])
    position_values.append(self.__format_percentage_to_string(position.intraday_plpc * 100))
    return position_values
    
  def format_main_content(self):
    ''' Returns a list containing formatted values for 
    [0] Equity, [1] Daily Change, [2] Percent Change, [3] Buying Power 
    '''
    return [ '{:,.2f}'.format(self.get_stock_equity()),
              self.__format_dollars_to_string(self.get_account_daily_change()),
              self.__format_percentage_to_string(self.get_account_percent_change()),
              '{:,.2f}'.format(self.get_buying_power()) ]


  def create_plot_html(self) -> str:
    ''' Creates the graph html div and returns it in string form using equities and times '''
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
      f.write(fig.to_html(include_plotlyjs='cdn', default_width="100%", default_height="600px", config={"displayModeBar": False}))
    with open('./templates/graph.html', 'r') as graph:
      graph.readline()
      graph.readline()
      graph.readline()
      graph_div = graph.readline()
      graph_div += graph.readline()
    os.remove('./templates/graph.html')
    return graph_div

  def create_site_html(self) -> str:
    ''' Puts together everything else to generate webpage '''
    with open("templates/index.html", "w") as html_file:
      html_file.write(webpage.DOCTYPE)
      html_file.write(webpage.HEAD)
      html_file.write(webpage.NAVBAR)
      content = self.format_main_content()
      graph_div = self.create_plot_html()
      primary_body = webpage.add_primary_content_body(content[0], content[1], content[2], graph_div, content[3])
      html_file.write(primary_body)
      decisions = webpage.get_decisions()
      html_file.write(webpage.ABOUT)
      for x in range(5):
        html = webpage.pull_recent_news(decisions[x])
        for line in html:
          html_file.write(line)
      html_file.write(webpage.NEWS)
      html_file.write(webpage.CONTACT)

WDR = WebpageDataRefresher()
WDR.create_site_html()
