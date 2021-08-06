from config import *
from .decision import Decision
from database_scripts import queries

DOCTYPE = '''<!DOCTYPE html>'''
HEAD = '''
  <head>
    <link rel="stylesheet" href="/static/styles.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://use.typekit.net/oxi4xqh.css">
    <title>QuantBot</title>
    <link rel="shortcut icon" href="/static/favicon.ico">
    <script type="text/javascript">
      window.onload = function () {
        CanvasJS.addColorSet("yellowShades",
        [
          "#FFBF00",
          "#E1C16E",
          "#FFEA00",
          "#FDDA0D",
          "#FFFF8F",
          "#DFFF00",
          "#E4D00A",
          "#8B8000",
          "#FFD700",
          "#FFC000",
          "#DAA520",
          "#FCF55F",
          "#FAFA33",
          "#F4BB44",
          "#FBEC5D",
          "#FFFFF0",
          "#FFFAA0",
          "	#F4C430",
          "	#F3E5AB",
          "#FFFF00",
          "	#FFAA33",
          "	#C4B454"
        ]);
        var chart = new CanvasJS.Chart("chartContainer",
        {
          colorSet: "yellowShades",
          title:{
            text:"Breakdown by Stock",
            fontColor: "white",
            margin: 10
          },

          theme: "dark2",
          backgroundColor: "black",
          height: 350,
          width: 350,
          toolTip:{
            content: "{indexLabel}: {y}%",
            enabled: true,       //disable here
            animationEnabled: true //disable here
          },
          data: [
          {
            type: "pie",
            indexLabelFontColor: "black",
            indexLabelPlacement: "inside",
            showInLegend: false,
            legendText: "{indexLabel}",
            dataPoints: [
              {% for holding in holdings %}
                {  y: {{holding[10]}}, indexLabel: "{{holding[0]}}" },
              {% endfor %}
              {y: 0, indexLabel: ""}
            ]
          }
          ]
        });
        chart.render();

        var chart2 = new CanvasJS.Chart("chartContainer2",
        {
          colorSet: "yellowShades",
          title:{
            text:"Breakdown by Category",
            fontColor: "white",
            margin: 10
          },

          theme: "dark2",
          backgroundColor: "black",
          height: 350,
          width: 350,
          toolTip:{
            content: "{indexLabel}: {y}%",
            enabled: true,       //disable here
            animationEnabled: true //disable here
          },
          data: [
          {
            type: "pie",
            indexLabelFontColor: "black",
            indexLabelPlacement: "inside",
            indexLabelFontSize: 12,
            indexLabelMaxWidth: 200, 
            showInLegend: false,
            indexLabelWrap: false,
            legendText: "{indexLabel}",
            dataPoints: [
              {% for key, value in cats.items() %}
                {  y: {{value}}, indexLabel: "{{key}}" },
              {% endfor %}
              {y: 0, indexLabel: ""}
            ]
          }
          ]
        });
        chart2.render();
      }
    </script>
    <script type="text/javascript" src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
  </head>
  <body style="overflow-x: hidden">
'''

NAVBAR = '''
    <div class="nav-bar">
      <a href="/">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="/static/logo.mp4" type="video/mp4">
      </video>
    </a>
      <ul class="nav-buttons">
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="/portfolio">Portfolio</a></li>
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

TOPHALF = '''
  <div class="plpcs" style="width: 100%; position: relative; left: -5%; margin-bottom: 40px">
  <p style="position: relative; left: 6.5%; color: yellow; font-size: 18px">Today's Biggest Movers</p>
  <style>
    .zoom {
      transition: transform .1s; /* Animation */
      z-index: 20;
      -webkit-box-shadow: 0px 4px 14px 0px rgba(66,66,66,0.38); 
      box-shadow: 0px 4px 14px 0px rgba(66,66,66,0.38);
    }
    .zoom:hover {
      transform: scale(1.2); /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
      cursor: pointer;
      z-index: 25;
      opacity: 100%;
      -webkit-box-shadow: 0px 10px 13px -7px #000000, 5px 10px 8px 10px rgba(0,0,0,0.42); 
      box-shadow: 0px 10px 13px -7px #000000, 5px 10px 8px 10px rgba(0,0,0,0.42);
    }
  </style>
    <ul class="outer-list" style="list-style: none; font-size: 15px;">
      <li>
        <ul class="inner-list" style="list-style: none; display: flex; flex-direction: horizontal">
'''

BOTTOMHALF = '''
        </ul>
      </li>
      <li>
        <ul  class="inner-list" style="list-style: none; display: flex; flex-direction: horizontal; margin-top: 15px">
'''

ENDOFPLPC = '''
        </ul>
      </li>
    </ul>
  </div>
'''


# just show ticker and plpc centered, when hovering, shift content to the left and on the right show price and our holdings

def get_winner(plpc):
  #width = str(25 + float(500 * abs(plpc.intraday_plpc))) + "%"
  opacity = str(60 + float(10000 * abs(plpc.intraday_plpc))) + "%"
  if (plpc.intraday_plpc * 100) >= 0 and (plpc.intraday_plpc * 100) < 1:
    color = "rgba(2, 66, 0, 1)"
  elif (plpc.intraday_plpc * 100) >= 1 and (plpc.intraday_plpc * 100) < 1.5:
    color = "rgba(24, 152, 22, 1)"
  elif (plpc.intraday_plpc * 100) >= 1.5:
    color = "rgba(3, 255, 0, 0.85)"

  if (plpc.intraday_plpc * 100) < 0 and (plpc.intraday_plpc * 100) > -1:
    color = "rgba(144, 0, 0, 0.85)"
  elif (plpc.intraday_plpc * 100) <= -1 and (plpc.intraday_plpc * 100) > -1.5:
    color = "rgba(174, 0, 0, 1)"
  elif (plpc.intraday_plpc * 100) <= -1.5:
    color = "red"

  return f'''
    <li class="zoom" style="width: 25%; background-color: {color}; opacity: {opacity}; color: white; list-style: none; margin-right: 15px; height: 80px;">
    <a style="color: white; text-decoration: none; width: 100%" href="https://www.marketwatch.com/investing/stock/{plpc.symbol}" target="_blank">
      <ul class = "tile" style="list-style: none; position: relative; left: -10%; top: 5%">
        <li style="display: flex; flex-direction: horizontal; margin-bottom: -25px"><p class="left-col">{plpc.symbol}</p><p class="right-col" style="position: absolute; right: 5%; margin-bottom: -65px; text-align: right">${"{:.2f}".format(plpc.current_price)}</p></li>
        <li><p class="left-col">{str(round(plpc.intraday_plpc * 100, 2))}%</p></li>
      </ul>
    </a>
    </li>
  '''  

def get_decisions():
  decisions = []
  CURSOR.execute(queries.SELECT_LAST10_DECISIONS)
  for row in CURSOR.fetchall():
    decisions.append(Decision(row[1], row[2], row[3], row[4], row[5], row[6]))
  
  print(decisions)
  return decisions

def pull_recent_news(d : 'Decision') -> 'str':
  phrases = [ "This article led the bot to " + d.decision + " " + str(d.shares_moved) + " shares of " + d.symbol + ".", 
              "As a result of this article, QuantBot decided to " + d.decision + " " + str(d.shares_moved) + " shares of " + d.symbol + ".", 
              "An order to " + d.decision + " " + str(d.shares_moved) + " shares of " + d.symbol + " was created due to this article." ]
  
  return  f"""
          <a href={d.url} target="_blank" style=" text-decoration: none;"><li class="article">
            <ul class="inner-article">
              <li class="article-words">
                <p class="article-p" style="color: white; font-size: 16px">{d.title}</p>
                <p class="article-intro" style="color: white; font-size: 14px">"{d.intro}..."</p>
                <p class="article-summary color" style="font-size: 15px; margin-top: 25px">QuantBot decided to {d.decision} {d.shares_moved} shares of {d.symbol}.</p>
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
    '''
NEWSTART = '''
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