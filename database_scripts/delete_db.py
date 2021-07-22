from sqlite3.dbapi2 import OperationalError
import __init__
import queries
from config import *

try:
  CURSOR.execute(queries.DROP_STOCK_TABLE)
  CURSOR.execute(queries.DROP_PRICE_TABLE)
  CURSOR.execute(queries.DROP_NEWS_TABLE)
  CURSOR.execute(queries.DROP_SENTIMENT_TABLE)
  CURSOR.execute(queries.DROP_TIMESERIES_TABLE)
  CURSOR.execute(queries.DROP_DECISIONS_TABLE)
except OperationalError as OE:
  print(OE)
finally:
  CONNECTION.commit()
