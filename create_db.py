import sqlite3

connection = sqlite3.connect('databases/stock-data.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment_data (
        word PRIMARY KEY, 
        category NOT NULL,
        sentiment NOT NULL,
        frequency INTEGER NOT NULL,
        stock_id INTEGER,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_series_data (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        symbol TEXT,
        mape FLOAT NOT NULL,
        one_week_fc FLOAT NOT NULL,
        one_month_fc FLOAT NOT NULL,
        one_week_actual FLOAT NOT NULL,
        one_month_actual FLOAT NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_news (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date_retrieved NOT NULL,
        url NOT NULL,
        analyzed BIT NOT NULL,
        article_content NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

connection.commit()

