# Where the actual bot will live and operate

from data_retriever import DataRetriever
from trader import Trader
from flask import Flask

class QuantBot:
  def __init__(self):
    pass


app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 8000

@app.route('/')
def main():
  ''' Start a server '''
  print(f"Starting server on {HOST}:{PORT}")
  return "Started"

if __name__ == '__main__':
  app.run(HOST, PORT)