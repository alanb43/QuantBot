import sqlite3
connection = sqlite3.connect('databases/stock-data.db')
    
cursor = connection.cursor()
cursor.execute("""
    DROP TABLE stock_price
""")
cursor.execute("""
    DROP TABLE stock
""")
connection.commit()