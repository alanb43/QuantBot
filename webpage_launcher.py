from trader import *
import webbrowser
import time

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Get our account information.
account = api.get_account()

EQUITY = float(account.equity)
EQUITY = "{:,.2f}".format(EQUITY)

aapl_position = api.get_position('AAPL')
tsla_position = api.get_position('TSLA')
googl_position = api.get_position('GOOGL')

DAILY_CHANGE = float(googl_position.unrealized_intraday_pl) + float(tsla_position.unrealized_intraday_pl) + float(aapl_position.unrealized_intraday_pl)
DAILY_CHANGE = "{:,.2f}".format(DAILY_CHANGE)
if DAILY_CHANGE[0] == "-":
    DAILY_CHANGE = str(DAILY_CHANGE)
    DAILY_CHANGE = "-$" + DAILY_CHANGE[1:]
else:
    DAILY_CHANGE = "+$" + DAILY_CHANGE

BUYING_POWER = float(account.buying_power)
BUYING_POWER = "{:,.2f}".format(BUYING_POWER)
PERCHANGE = ((float(account.equity) - float(account.last_equity)) / float(account.last_equity)) * 100
PERCHANGE = "{:.2f}".format(PERCHANGE)
if float(PERCHANGE) > 0:
    PERCHANGE = "+" + PERCHANGE

AAPL_VALUE = float(aapl_position.current_price)
AAPL_VALUE = "{:,.2f}".format(AAPL_VALUE)
if AAPL_VALUE[0] == "-":
  AAPL_VALUE = "-$" + AAPL_VALUE[1:]
else:
  AAPL_VALUE = "$" + AAPL_VALUE

AAPL_PERCHANGE = ((float(aapl_position.current_price) - float(aapl_position.lastday_price)) / float(aapl_position.lastday_price)) * 100
AAPL_PERCHANGE = "{:.2f}".format(AAPL_PERCHANGE)
if AAPL_PERCHANGE[0] == "-":
  AAPL_COLOR = "red"
elif float(AAPL_PERCHANGE) > 0:
  AAPL_COLOR = "green"
else:
  AAPL_COLOR = "white"

TSLA_VALUE = float(tsla_position.current_price)
TSLA_VALUE = "{:,.2f}".format(TSLA_VALUE)
if TSLA_VALUE[0] == "-":
    TSLA_VALUE = "-$" + TSLA_VALUE[1:]
else:
    TSLA_VALUE = "$" + TSLA_VALUE

TSLA_PERCHANGE = ((float(tsla_position.current_price) - float(tsla_position.lastday_price)) / float(tsla_position.lastday_price)) * 100
TSLA_PERCHANGE = "{:.2f}".format(TSLA_PERCHANGE)
if TSLA_PERCHANGE[0] == "-":
  TSLA_COLOR = "red"
elif float(TSLA_PERCHANGE) > 0:
  TSLA_COLOR = "green"
else:
  TSLA_COLOR = "white"

GOOGL_VALUE = float(googl_position.current_price)
GOOGL_VALUE = "{:,.2f}".format(GOOGL_VALUE)
if GOOGL_VALUE[0] == "-":
    GOOGL_VALUE = "-$" + GOOGL_VALUE[1:]
else:
    GOOGL_VALUE = "$" + GOOGL_VALUE

GOOGL_PERCHANGE = ((float(googl_position.current_price) - float(googl_position.lastday_price)) / float(googl_position.lastday_price)) * 100
GOOGL_PERCHANGE = "{:.2f}".format(GOOGL_PERCHANGE)
if GOOGL_PERCHANGE[0] == "-":
  GOOGL_COLOR = "red"
elif float(GOOGL_PERCHANGE) > 0:
  GOOGL_COLOR = "green"
else:
  GOOGL_COLOR = "white"

html_content = f"""<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="styles.css">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
  <title>QuantBot</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
<body>
  <div class="nav-bar">
    <a href="#top">
    <video disableRemotePlayback autoplay muted loop id="myVideo">
      <source src="logo.mp4" type="video/mp4">
    </video>
  </a>
    <ul class="nav-buttons">
      <li class="button color"><a style = "text-decoration: none; color: inherit" href="#top">Portfolio</a></li>
      <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
      <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
    </ul>
  </div>
  <div class="side-bar">
    <ul class="shares">
      <li class="share">
        <ul class="share-details">
          <li>AAPL</li>
          <li class="value"><p>{AAPL_VALUE}</p><p class="per" style="color: {AAPL_COLOR}">{AAPL_PERCHANGE}%</p></li>
        </ul>
      </li>
      <li class="share">
        <ul class="share-details">
          <li>TSLA</li>
          <li class="value"><p>{TSLA_VALUE}</p><p class="per" style="color: {TSLA_COLOR}">{TSLA_PERCHANGE}%</p></li>
        </ul>
      </li>
      <li class="share">
        <ul class="share-details">
          <li>GOOGL</li>
          <li class="value"><p>{GOOGL_VALUE}</p><p class="per" style="color: {GOOGL_COLOR}">{GOOGL_PERCHANGE}%</p></li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="body">
    <h1 id="top">${EQUITY}</h1>
    <h2 class="color">{DAILY_CHANGE} ({PERCHANGE}%) Today</h2>
    <img src="fakegraph.png" alt="graph" class="fakegraph">
    <div class="buyingpower">
        <p class="buy">Buying Power</p>
        <p class="buy2">${BUYING_POWER}</p>
    </div>
    <div class="summary">
      <p class="color">What is Quantbot?</p>
      <p class="des">Quantbot is a Python Bot that utilizes a combination of machine learning, time analysis, and sentiment analysis to automatically buy and sell stocks. The bot uses a web scraper that periodically checks for new articles regarding a company and analyzes the content in the article. If the bot deems the article particularly positive or negative for that company, the bot will either buy or sell the shares we have.</p>
    </div>
    <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
    <div class="news">
      <ul class="news-list">
        <li class="article">
          <ul class="inner-article">
            <li>
              <img src="a.png" alt="graph" class="article-img">
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
              <img src="a.png" alt="graph" class="article-img">
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
              <img src="a.png" alt="graph" class="article-img">
            </li>
            <li class="article-words">
              <p class="article-summary color">This article led to the bot buying 15 shares of TSLA.</p>
              <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="contact color" id="contact">
      <h3 style="margin-bottom: -10px; font-size: 18px;">Contact Us</h3>
      <p style="margin-bottom: -10px; font-size: 15px;">Josh Cunningham || jcun@umich.edu || LinkedIn</p>
      <p style="font-size: 15px">Alan Bergsneider || bera@umich.edu || LinkedIn</p>
    </div>
  </div>

</body>"""

with open("webpage/index.html", "w") as html_file:
    html_file.write(html_content)

time.sleep(2)
