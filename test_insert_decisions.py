from database_scripts import queries
from models.decision import Decision
from config import *


d = Decision("AAPL", "Buy", 4, "https.link.com", "Article Title", "Long winded introduction              ")
CURSOR.execute(queries.INSERT_DECISION, (d.symbol, d.decision, d.shares_moved, d.url, d.title, d.intro))
d = Decision("GOOGL", "Sell", 4, "https.link.com", "Article Title", "Long winded introduction              ")
CURSOR.execute(queries.INSERT_DECISION, (d.symbol, d.decision, d.shares_moved, d.url, d.title, d.intro))
d = Decision("FART", "Buy", 4, "https.link.com", "Article Title", "Long winded introduction              ")
CURSOR.execute(queries.INSERT_DECISION, (d.symbol, d.decision, d.shares_moved, d.url, d.title, d.intro))

CONNECTION.commit()