# Where the actual bot will live and operate

from data_retriever import *
from trader import *
from flask import Flask

app = Flask(__name__)

@app.route('/')

def main():
  return "<h1>QuantBot.io</h1>"
