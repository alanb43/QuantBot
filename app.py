from data_retriever import DataRetriever
from flask import Flask, render_template
from webpage_data_refresher import WebpageDataRefresher
from trader import Trader
import csv

T = Trader()
data = T.create_market_order_data("AMD", 5, "buy", "market", "day")
#T.place_order(data)

app = Flask(__name__)


def ticker_dict():
  company_industry = {}
  with open('symbols.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      company_industry[row[1]] = row[2].replace(' ','_')

  return company_industry


@app.route("/")
def index():
  WDR = WebpageDataRefresher()
  WDR.create_site_html()
  stocks = WDR.positions
  sorted_by_plpc = WDR.plpc_sorted_holdings
  print(ticker_dict())
  return render_template('index.html', stocks=stocks, plpc_sorted=sorted_by_plpc)


@app.route("/OOGABOOGA")
def ooga():
  T = Trader()
  data = T.create_market_order_data("AMD", 5, "buy", "market", "day")
  T.place_order(data)

if __name__ == "__main__":
  app.run(host="localhost", debug=True)



