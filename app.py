from data_retriever import DataRetriever
from flask import Flask, render_template
from webpage_data_refresher import WebpageDataRefresher
from trader import Trader
import time

T = Trader()
data = T.create_market_order_data("AMD", 5, "buy", "market", "day")
#T.place_order(data)

app = Flask(__name__)


def ticker_dict(): # open symbols.csv, make matrix containing ticker, category
  pass


@app.route("/")
def index():
  WDR = WebpageDataRefresher()
  WDR.create_site_html()
  stocks = WDR.positions
  return render_template('index.html', stocks=stocks)


@app.route("/OOGABOOGA")
def ooga():
  T = Trader()
  data = T.create_market_order_data("AMD", 5, "buy", "market", "day")
  T.place_order(data)

if __name__ == "__main__":
  app.run(host="localhost", debug=True)



