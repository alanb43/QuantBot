from trader import *
from flask import Flask, render_template

application = Flask(__name__)

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Get our account information.
account = api.get_account()

aapl_position = api.get_position('AAPL')
tsla_position = api.get_position('TSLA')

EQUITY = account.equity
DAILY_CHANGE = str(float(account.equity) - float(account.last_equity))
if float(DAILY_CHANGE) < 0:
    DAILY_CHANGE = "-$" + DAILY_CHANGE[1:]
else:
    DAILY_CHANGE = "+$" + DAILY_CHANGE
BUYING_POWER = account.buying_power
PERCHANGE = str(((float(account.equity) - float(account.last_equity)) / float(account.last_equity)) * 100)
if float(PERCHANGE) > 0:
    PERCHANGE = "+" + PERCHANGE

AAPL_VALUE = aapl_position.market_value
if float(AAPL_VALUE) < 0:
    AAPL_VALUE = "-$" + AAPL_VALUE[1:]
else:
    AAPL_VALUE = "+$" + AAPL_VALUE
AAPL_PERCHANGE = str(((float(aapl_position.current_price) - float(aapl_position.lastday_price)) / float(aapl_position.lastday_price)) * 100)
if float(AAPL_PERCHANGE) > 0:
    AAPL_PERCHANGE = "+" + AAPL_PERCHANGE

TSLA_VALUE = tsla_position.market_value
if float(TSLA_VALUE) < 0:
    TSLA_VALUE = "-$" + TSLA_VALUE[1:]
else:
    TSLA_VALUE = "+$" + TSLA_VALUE
TSLA_PERCHANGE = str(((float(tsla_position.current_price) - float(tsla_position.lastday_price)) / float(tsla_position.lastday_price)) * 100)
if float(TSLA_PERCHANGE) > 0:
    TSLA_PERCHANGE = "+" + TSLA_PERCHANGE

class Main:
    equity=EQUITY
    daily_change=DAILY_CHANGE, 
    perchange=PERCHANGE,
    buyingpower = BUYING_POWER,
    aapl_per = AAPL_PERCHANGE,
    aapl = AAPL_VALUE,
    tsla = TSLA_VALUE,
    tsla_per = TSLA_PERCHANGE

@application.route("/", methods=['GET'])
def home():
    return render_template('index.html',     
    equity=EQUITY,
    daily_change=DAILY_CHANGE, 
    perchange=PERCHANGE,
    buyingpower = BUYING_POWER,
    aapl_per = AAPL_PERCHANGE,
    aapl = AAPL_VALUE,
    tsla = TSLA_VALUE,
    tsla_per = TSLA_PERCHANGE)