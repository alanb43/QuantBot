import random

DOCTYPE = '''<!DOCTYPE html>'''
HEAD = '''
  <head>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://use.typekit.net/oxi4xqh.css">
    <title>QuantBot</title>
    <link rel="shortcut icon" href="resources/favicon.ico">
  </head>
  <body>
'''

NAVBAR = '''
    <div class="nav-bar">
      <a href="QuantBot.io">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="resources/logo.mp4" type="video/mp4">
      </video>
    </a>
      <ul class="nav-buttons">
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#top">Portfolio</a></li>
        <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
      </ul>
    </div>
'''

SIDEBAR = '''
    <div class="side-bar">
      <p class="holdings">Current Holdings</p>
      <ul class="shares">
'''

def add_sidebar_holding(symbol, qty, price, color, percent):
  return f'''
        <li class="share">
          <ul class="share-details">
            <li ><p style="margin-bottom: -10px; top: -40%;">{symbol}</p><p class="quantity">{qty} Shares</p></li>
            <li class="value"><p class="num">${price}</p><p class="per num" style="color: {color}; font-weight: bold">{percent}%</p></li>
          </ul>
        </li>
  '''

END_SIDEBAR = '''
      </ul>
    </div>
'''
def add_primary_content_body(equity, dailychange, percentchange, graph, buyingpower):
  return f'''
    <div class="body">
      <h1 id="top" class="num">${equity}</h1>
      <h2 class="color num">{dailychange} ({percentchange}%)</h2>
      {graph}
      <div class="buyingpower">
          <p class="buy">Buying Power</p>
          <p class="buy2 num">${buyingpower}</p>
      </div>
  '''

def get_decisions():
  decisions = []
  with open('./models/decisions.txt', 'r') as d:
    lines = d.readlines()
    x = 0
    decision = []
    for line in lines:
      if x == 5:
        decisions.append(decision)
        decision = []
        x = 0
      decision.append(line)
      x += 1
  decisions.append(decision)
  return [ele for ele in reversed(decisions)]

def pull_recent_news(decision) -> str:
  phrases = ["This article led the bot to " + decision[1] + " " + decision[2] + " shares of " + decision[0] + ".", "As a result of this article, QuantBot decided to " + decision[1] + " " + decision[2] + " shares of " + decision[0] + ".", "An order to " + decision[1] + " " + decision[2] + " shares of " + decision[0] + " was created due to this article."]
  return  f"""
          <a href={decision[4]} target="_blank" style=" text-decoration: none;"><li class="article">
            <ul class="inner-article">
              <li class="article-words">
                <p class="article-p color" style="font-size: 16px">Article: {decision[3]}</p>
                <p class="article-intro" style="color: white; font-size: 12px">"random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence random sentence..."</p>
                <p class="article-summary color" style="font-size: 15px; margin-top: 25px">{phrases[random.randint(0,len(phrases)-1)]}</p>
              </li>
            </ul>
          </li></a>
    """


ABOUT = '''
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
'''

NEWS = '''
        </ul>
      </div>
'''

CONTACT = '''
      <div class="contact color" id="contact">
        <h3 style="margin-bottom: -10px; font-size: 18px;">Contact Us</h3>
        <p style="margin-bottom: -10px; font-size: 15px;">Josh Cunningham || jcun@umich.edu || LinkedIn</p>
        <p style="font-size: 15px">Alan Bergsneider || bera@umich.edu || LinkedIn</p>
      </div>
    </div>
  </body>
'''


get_decisions()