import alpaca_trade_api as tradeapi
import time

key = "PKG1174VEQRPR6K8TTBV"
sec = "rg8yxCn2LgsrBXUYtR1zhhm9XV0PWeIGEy8DMFMX"

url = "https://paper-api.alpaca.markets"

api = tradeapi.REST(key, sec, url, api_version='v2')

account = api.get_account()
print(account.status)

