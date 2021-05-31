from trader import *

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Get our account information.
account = api.get_account()

aapl_position = api.get_position('AAPL')
tsla_position = api.get_position('TSLA')

EQUITY = account.equity
DAILY_CHANGE = str(float(account.equity) - float(account.last_equity))
BUYING_POWER = account.buying_power
PERCHANGE = str(((float(account.equity) - float(account.last_equity)) / float(account.last_equity)) * 100)

AAPL_VALUE = aapl_position.market_value
AAPL_PERCHANGE = str(((float(aapl_position.current_price) - float(aapl_position.lastday_price)) / (aapl_position.lastday_price)) * 100)

TSLA_VALUE = tsla_position.market_value
TSLA_PERCHANGE = str(((float(tsla_position.current_price) - float(tsla_position.lastday_price)) / (tsla_position.lastday_price)) * 100)

