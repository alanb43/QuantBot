import __init__
import queries
from config import *
from account_data_retriever import AccountDataRetriever
import csv

ADR = AccountDataRetriever()

company_industry = {}
with open('symbols.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    company_industry[row[1]] = row[2].replace(' ','_')

# For when new stocks need to be added to stock schema
for stock in ADR.positions:
  try:
    CURSOR.execute(queries.INSERT_STOCK, (stock.symbol, company_industry[stock.symbol]))
  except Exception as e:
    print(e)

CONNECTION.commit()