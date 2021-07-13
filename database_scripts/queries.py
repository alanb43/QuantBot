# Constant queries, change them here and everywhere will be updated at once.

# For selecting data within database

SELECT_STOCK_WITH_ID = """SELECT * FROM stock WHERE id = ?"""

SELECT_ALL_SENTIMENT_DATA = """SELECT * FROM sentiment_data"""

SELECT_WORD_SENTIMENT_DATUM = """SELECT * FROM sentiment_data WHERE word = ?"""

SELECT_NEWS_WITH_URL = """SELECT * FROM stock_news WHERE url = ?"""

EXISTS_NEWS_WITH_URL = f"""SELECT EXISTS({SELECT_NEWS_WITH_URL})"""

SELECT_TOTAL_NUM_ARTICLES = """SELECT COUNT(*) FROM stock_news"""

SELECT_POS_NUM_ARTICLES = """SELECT COUNT(*) FROM stock_news WHERE sentiment = 'Positive'"""

SELECT_NEG_NUM_ARTICLES = """SELECT COUNT(*) FROM stock_news WHERE sentiment = 'Negative'"""

SELECT_UNANALYZED_ARTICLES = """SELECT stock_id, article_content FROM stock_news WHERE analyzed = 0"""

# For updating database with new data
UPDATE_SENTIMENT = """UPDATE sentiment_data SET positive_freq = ?, negative_freq = ?, frequency = ? WHERE word = ?"""

UPDATE_SENTIMENT_CATEGORY = """UPDATE sentiment_data SET category = ?"""


# For INSERTING into database 
INSERT_STOCK = """INSERT INTO stock (symbol, category) VALUES (?, ?)"""

INSERT_STOCK_PRICE = """INSERT INTO stock_price (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)"""

INSERT_NEWS_ARTICLE = """INSERT INTO stock_news (stock_id, title, date_retrieved, url, analyzed, sentiment, article_content) VALUES (?, ?, ?, ?, ?, ?, ?)"""

INSERT_SENTIMENT_DATUM = """INSERT INTO sentiment_data (word, category, positive_freq, negative_freq, frequency) VALUES (?, ?, ?, ?, ?)"""

# For creating database tables
CREATE_STOCK_TABLE = """CREATE TABLE IF NOT EXISTS stock (id INTEGER PRIMARY KEY, symbol TEXT NOT NULL UNIQUE, category TEXT)"""

CREATE_PRICE_TABLE = """CREATE TABLE IF NOT EXISTS stock_price (id INTEGER PRIMARY KEY, stock_id INTEGER, date NOT NULL, open NOT NULL, 
                        high NOT NULL, low NOT NULL, close NOT NULL, volume NOT NULL, FOREIGN KEY (stock_id) REFERENCES stock (id))"""

CREATE_NEWS_TABLE = """CREATE TABLE IF NOT EXISTS stock_news (id INTEGER PRIMARY KEY, stock_id INTEGER, title NOT NULL, date_retrieved NOT NULL,
                       url UNIQUE NOT NULL, analyzed BIT NOT NULL, sentiment, article_content NOT NULL, FOREIGN KEY (stock_id) REFERENCES stock (id))"""

CREATE_SENTIMENT_TABLE = """CREATE TABLE IF NOT EXISTS sentiment_data (word PRIMARY KEY, category NOT NULL, positive_freq INTEGER NOT NULL, negative_freq
                            INTEGER NOT NULL, frequency INTEGER NOT NULL, FOREIGN KEY (category) REFERENCES stock (category))"""

CREATE_TIMESERIES_TABLE = """CREATE TABLE IF NOT EXISTS time_series_data (id INTEGER PRIMARY KEY, stock_id INTEGER, symbol TEXT, mape FLOAT NOT NULL,
                             one_week_fc FLOAT NOT NULL, one_month_fc FLOAT NOT NULL, one_week_actual FLOAT NOT NULL, one_month_actual FLOAT NOT NULL,
                             FOREIGN KEY (stock_id) REFERENCES stock (id))"""

# For deleting database tables
DROP_STOCK_TABLE = """DROP TABLE stock"""

DROP_PRICE_TABLE = """DROP TABLE stock_price"""

DROP_NEWS_TABLE = """DROP TABLE stock_news"""

DROP_SENTIMENT_TABLE = """DROP TABLE sentiment_data"""

DROP_TIMESERIES_TABLE = """DROP TABLE time_series_data"""
