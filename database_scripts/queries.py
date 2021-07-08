# Constant queries, change them here and everywhere will be updated at once.

# For updating database with new data
INSERT_STOCK = """INSERT INTO stock (symbol, category) VALUES (?, ?)"""

INSERT_STOCK_PRICE = """INSERT INTO stock_price (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)"""

INSERT_NEWS_ARTICLE = """INSERT INTO stock_news (stock_id, title, date_retrieved, url, analyzed, article_content) VALUES (?, ?, ?, ?, ?, ?)"""

# For creating database tables
CREATE_STOCK_TABLE = """CREATE TABLE IF NOT EXISTS stock (id INTEGER PRIMARY KEY, symbol TEXT NOT NULL UNIQUE, category TEXT)"""

CREATE_PRICE_TABLE = """CREATE TABLE IF NOT EXISTS stock_price (id INTEGER PRIMARY KEY, stock_id INTEGER, date NOT NULL, open NOT NULL, 
                        high NOT NULL, low NOT NULL, close NOT NULL, volume NOT NULL, FOREIGN KEY (stock_id) REFERENCES stock (id))"""

CREATE_NEWS_TABLE = """CREATE TABLE IF NOT EXISTS stock_news (id INTEGER PRIMARY KEY, stock_id INTEGER, title NOT NULL, date_retrieved NOT NULL,
                       url UNIQUE NOT NULL, analyzed BIT NOT NULL, article_content NOT NULL, FOREIGN KEY (stock_id) REFERENCES stock (id))"""

CREATE_SENTIMENT_TABLE = """CREATE TABLE IF NOT EXISTS sentiment_data (word PRIMARY KEY, category NOT NULL, sentiment NOT NULL,
                            frequency INTEGER NOT NULL, stock_id INTEGER, FOREIGN KEY (stock_id) REFERENCES stock (id))"""

CREATE_TIMESERIES_TABLE = """CREATE TABLE IF NOT EXISTS time_series_data (id INTEGER PRIMARY KEY, stock_id INTEGER, symbol TEXT, mape FLOAT NOT NULL,
                             one_week_fc FLOAT NOT NULL, one_month_fc FLOAT NOT NULL, one_week_actual FLOAT NOT NULL, one_month_actual FLOAT NOT NULL,
                             FOREIGN KEY (stock_id) REFERENCES stock (id))"""

# For deleting database tables
DROP_STOCK_TABLE = """DROP TABLE stock"""
DROP_PRICE_TABLE = """DROP TABLE stock_price"""
DROP_NEWS_TABLE = """DROP TABLE stock_news"""
DROP_SENTIMENT_TABLE = """DROP TABLE sentiment_data"""
DROP_TIMESERIES_TABLE = """DROP TABLE time_series_data"""