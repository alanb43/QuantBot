import __init__
import queries
from config import *
from article_retriever import ArticleRetriever
from datetime import date

# Get symbols and IDs to use as keys in table
CURSOR.execute(queries.SELECT_STOCK_ID_AND_SYMBOL)
rows = CURSOR.fetchall()
symbols = []
stock_ids = {}
for row in rows:
  symbol = row['symbol']
  symbols.append(symbol)
  stock_ids[symbol] = row['id']

AR = ArticleRetriever()

for symbol in symbols:
  print(f"{symbol}'s news articles are being processed.")
  stock_id = stock_ids[symbol]
  articles = AR.get_stock_news(symbol)
  # DISABLE THIS IN PRODUCTION THIS IS FOR TESTING WITH SENTIMENT
  articles_added = 0
  for article in articles:
    # DISABLE
    if articles_added == 3:
      break
    try:
      CURSOR.execute(queries.INSERT_NEWS_ARTICLE, (stock_id, article.title, date.today(), article.url, 0, None, article.contents))
      CONNECTION.commit()
      articles_added += 1 # DISABLE
    except:
      print(f"URL was in database: {article.url}")
