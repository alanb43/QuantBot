import sqlite3
from account_data_retriever import AccountDataRetriever
from data_retriever import DataRetriever
from datetime import date, timedelta



ADR = AccountDataRetriever()

connection = sqlite3.connect('databases/stock-data.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# For when new stocks need to be added to stock schema

# for stock in ADR.positions:
#   try:
#     cursor.execute("""INSERT INTO stock (symbol) VALUES (?)""", (stock.symbol,))
#   except:
#     print(f"{stock.symbol} was already in the database")

# connection.commit

cursor.execute("""SELECT id, symbol FROM stock""")
rows = cursor.fetchall()
symbols = []
stock_ids = {}
for row in rows:
  symbol = row['symbol']
  symbols.append(symbol)
  stock_ids[symbol] = row['id']

START_YEAR = "2021-01-01"

yesterday = date.today() - timedelta(1)
day_before_yesterday = yesterday - timedelta(1)

for symbol in symbols:
  stock_id = stock_ids[symbol]
  barsets = ADR.api.get_bars(symbol, start=day_before_yesterday, end=yesterday, timeframe=TimeFrame.Day)
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

connection.commit()
