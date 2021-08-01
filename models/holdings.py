from account_data_retriever import AccountDataRetriever
import models.webpage as webpage

ADR = AccountDataRetriever()

html_top_content = webpage.DOCTYPE + webpage.HEAD + '''
  
  <div class="nav-bar">
    <a href="/">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="/static/logo.mp4" type="video/mp4">
      </video>
    </a>
    <ul class="nav-buttons">
      <li class="button color"><a style = "text-decoration: none; color: white" href="#top">Portfolio</a></li>
      <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
      <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
    </ul>
  </div>
  <div class="scroll custom-scrollbar">
    <table class="holdings-table" style="background-color:#050505; border-collapse:collapse;">
      <tr style="text-align:center">
        <th>Stock</th>
        <th>Daily % Change</th>
        <th>Avg Cost</th>
        <th>Current Price</th>
        <th>Shares Owned</th>
        <th>Market Value</th>
        <th>Total P/L</th>
      </tr>
      {% for holding in holdings %}
      <tr style="text-align:center">
        <td>{{holding[0]}}</td>
        <td style="color:{{holding[7]}}">{{holding[1]}}</td>
        <td>{{holding[2]}}</td>
        <td>{{holding[3]}}</td>
        <td>{{holding[4]}}</td>
        <td>{{holding[5]}}</td>
        <td style="color:{{holding[8]}}">{{holding[6]}}</td>
      </tr>
      {% endfor %}
  </div>
'''


# Symbol, the cost I bought it at, its current price,
# the percentage of my portfolio it makes up, the percent change since purchasing,
# the daily percent change,  
def format_holding(holding, portfolio_value):
  symbol, qty, curr_price, avg_cost, day_pc, overall_pc, market_val = holding.symbol, holding.qty, holding.current_price, holding.cost, holding.intraday_plpc, holding.plpc, holding.market_value
  percent_of_portfolio = round(market_val / portfolio_value, 2)


  return f'''
  <tr style="height: 140px;">
  <a style="color: white; text-decoration: none; width: 100%" href="https://www.marketwatch.com/investing/stock/{holding.symbol}">

  </a>
  </tr>
  '''




  return f'''
    <li class="zoom" style="width: 25%; background-color: {color}; opacity: {opacity}; color: white; list-style: none; margin-right: 15px; height: 80px;">
    <a style="color: white; text-decoration: none; width: 100%" href="https://www.marketwatch.com/investing/stock/{plpc.symbol}" target="_blank">
      <ul class = "tile" style="list-style: none; position: relative; left: -5%; top: 5%">
        <li style="display: flex; flex-direction: horizontal; margin-bottom: -25px"><p class="left-col">{plpc.symbol}</p><p class="right-col" style="position: absolute; right: 5%; margin-bottom: -65px">${"{:.2f}".format(plpc.current_price)}</p></li>
        <li><p class="left-col">{str(round(plpc.intraday_plpc * 100, 2))}%</p><p class="right-col" style="position: absolute; right: 5%; top: 21px">${"{:.2f}".format(plpc.current_price * plpc.qty)}</p></li>
      </ul>
    </a>
    </li>
  '''  


def get_holdings():
  
  ADR = AccountDataRetriever()
  portfolio_value = ADR.get_stock_equity()
  # for holding in ADR.positions:
  #   result += format_holding(holding, portfolio_value)
  
  return  '''</table>'''
  





