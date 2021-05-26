# Where the actual bot will live and operate

from data_retriever import *
from trader import *
from flask import Flask

app = Flask(__name__)

@app.route('/')

def main():
  get_stock_prices('TSLA', '1y')
  get_stock_news('NHI')
  return "<h1>QuantBot.io</h1>"


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)