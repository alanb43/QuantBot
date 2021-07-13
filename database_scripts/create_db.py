import __init__
import queries
from config import *

CURSOR.execute(queries.CREATE_STOCK_TABLE)
CURSOR.execute(queries.CREATE_PRICE_TABLE)
CURSOR.execute(queries.CREATE_NEWS_TABLE)
CURSOR.execute(queries.CREATE_SENTIMENT_TABLE)
CURSOR.execute(queries.CREATE_TIMESERIES_TABLE)

CONNECTION.commit()

