from account_data_retriever import AccountDataRetriever
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
  ADR = AccountDataRetriever()
  cats = ADR.get_cats()
  return render_template('index.html', stocks=stocks, plpc_sorted=sorted_by_plpc, cats=cats)


@app.route("/portfolio")
def generate_portfolio_page():
  WDR = WebpageDataRefresher()
  WDR.create_portfolio_page()
  ADR = AccountDataRetriever()
  header = ["${:,.2f}".format(ADR.get_stock_equity())  ]
  holdings = ADR.formatted_positions
  cats = ADR.get_cats()
  return render_template('portfolio.html', header=header, holdings=holdings, cats=cats)


@app.route("/contact")
def generate_contact_page():
  return render_template('contact.html')

if __name__ == "__main__":
  app.run(host="localhost", debug=True)