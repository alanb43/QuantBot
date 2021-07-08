
from account_data_retriever import AccountDataRetriever
from data_retriever import DataRetriever
from models.timeframe import TimeFrame
from datetime import date, timedelta
from config import *

connection = sqlite3.connect('databases/stock-data.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


ADR = AccountDataRetriever()
DR = DataRetriever()

# For when new stocks need to be added to stock schema

# for stock in ADR.positions:
#   try:
#     cursor.execute("""INSERT INTO stock (symbol) VALUES (?)""", (stock.symbol,))
#   except:
#     pass

# connection.commit()

cursor.execute("""SELECT id, symbol FROM stock""")
rows = cursor.fetchall()
symbols = []
stock_ids = {}
for row in rows:
  symbol = row['symbol']
  symbols.append(symbol)
  stock_ids[symbol] = row['id']

START_YEAR = "2021-01-01"

today = date.today()
yesterday = today - timedelta(1)
day_before_yesterday = yesterday - timedelta(1)



for symbol in symbols:
  stock_id = stock_ids[symbol]
  print(f"{symbol} data is being processed")
  barsets = API.get_bars(symbol, start=START_YEAR, end=yesterday, timeframe=TimeFrame.Day)
  for bar in barsets:
    open = bar.o
    close = bar.c
    high = bar.h
    low = bar.l
    vol = bar.v
    date_ = bar.t.date()
    cursor.execute("""
      INSERT INTO stock_price (stock_id, date, open, high, low, close, volume) VALUES 
      (?, ?, ?, ?, ?, ?, ?)""", 
      (stock_id, date_, open, high, low, close, vol)
    )
  # articles = DR.get_stock_news(symbol)
  # for article in articles:
  #   try:
  #     cursor.execute("""
  #     INSERT INTO stock_news (stock_id, title, date_retrieved, url, analyzed, article_content) VALUES
  #     (?, ?, ?, ?, ?, ?)""", (stock_id, article.title, today, article.url, 0, article.contents)
  #     )
  #   except:
  #     print("URL was in database: ", article.url)
  connection.commit()
