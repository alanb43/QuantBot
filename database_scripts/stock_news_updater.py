import __init__
import queries
from config import *
from article_retriever import ArticleRetriever
from datetime import date

# Get symbols and IDs to use as keys in table
CURSOR.execute("""SELECT id, symbol FROM stock""")
rows = CURSOR.fetchall()
symbols = []
stock_ids = {}
for row in rows:
  symbol = row['symbol']
  symbols.append(symbol)
  stock_ids[symbol] = row['id']

AR = ArticleRetriever

for symbol in symbols:
  print(f"{symbol}'s news articles are being processed.")
  stock_id = stock_ids[symbol]
  articles = AR.get_stock_news(symbol)
  for article in articles:
    try:
      CURSOR.execute(queries.INSERT_NEWS_ARTICLE, (stock_id, article.title, date.today(), article.url, 0, None, article.contents))
    except:
      print(f"URL was in database: {article.url}")
  CONNECTION.commit()
