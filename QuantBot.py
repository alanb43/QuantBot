# Where the actual bot will live and operate

from data_retriever import *
from trader import *
import http.server
from flask import Flask

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