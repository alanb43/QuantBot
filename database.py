import sqlite3
from sqlite3 import Error

def create_connection(database_file):
  conn = None
  path = f"./databases/{database_file}"
  try:
    conn = sqlite3.connect(path)
    return conn  
  except Error as e:
    print(e)
  

def create_table(connection, sql_command):
  try:
    c = conn.cursor()
    c.execute(sql_command)
  except Error as e:
    print(e)


if __name__ == '__main__':
  conn = create_connection('symbols.db')


