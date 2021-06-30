import sqlite3
connection = sqlite3.connect('databases/stock-data.db')
    
cursor = connection.cursor()
cursor.execute("""DROP TABLE stock""")
cursor.execute("""DROP TABLE stock_price""")
cursor.execute("""DROP TABLE stock_news""")
cursor.execute("""DROP TABLE sentiment_data""")
cursor.execute("""DROP TABLE time_series_data""")

connection.commit()
