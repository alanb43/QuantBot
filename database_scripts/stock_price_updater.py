import __init__
import queries
from config import *
from models.timeframe import TimeFrame
from datetime import date, timedelta

# Get symbols and IDs to use as keys in table
CURSOR.execute("""SELECT id, symbol FROM stock""")
rows = CURSOR.fetchall()
symbols = []
stock_ids = {}
for row in rows:
  symbol = row['symbol']
  symbols.append(symbol)
  stock_ids[symbol] = row['id']

# Define a start date and end date for stock price data that will be stored
start_date = "2021-01-01"
end_date = date.today() - timedelta(days=1)
# this has to be updated each time the script is ran currently, will need to eventually turn this script 
# into a serverless function on cloud that's called daily with start and end being the same value (yesterday's prices) 

# the actual gathering of data and storing in the database
for symbol in symbols:
  print(f"{symbol} data is being processed")
  try:
    stock_id = stock_ids[symbol]
    barsets = API.get_bars(symbol, start=start_date, end=end_date, timeframe=TimeFrame.Day)
    for bar in barsets:
      open = bar.o
      close = bar.c
      high = bar.h
      low = bar.l
      vol = bar.v
      date_ = bar.t.date()
      CURSOR.execute(queries.INSERT_STOCK_PRICE, (stock_id, date_, open, high, low, close, vol))
  except:
    print(f"An error occurred when handling {symbol}.")
  finally:
    CONNECTION.commit()
