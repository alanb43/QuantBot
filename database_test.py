from mysql import connector
import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import *

def create_server_connection(host_name, user_name, user_password):
  '''
  REQUIRES: valid str representing host name, user name, user password
  EFFECTS:  attempts to establish a connection to the MySQL server / db
            prints error message if unsuccessful, returns valid connection
            or 'None' 
  '''
  # close any existing connections, avoid confusing the server
  connection = None 
  try:
    connection = mysql.connector.connect(
      host = host_name,
      user = user_name,
      passwd = user_password
    )
    print('MySQL Database connection successful')
  except Error as error:
    print(f"Error message: '{error}'")

  return connection

connection = create_server_connection('localhost', DATABASE_TEST_USER, DATABASE_TEST_PASS)

def create_database(connection, query):
  '''
  REQUIRES: connection from create_server_connection
  EFFECTS:  attempts to create a database, returns message on success / error
  '''
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    print("Database created successfully!")
  except Error as error:
    print(f"Error: '{error}'")

create_database_query = "CREATE DATABASE school"
create_database(connection, create_database_query)
