from polygon import RESTClient
import calendar

yy = 2021
mm = 5

print(calendar.month(yy,mm))


def main():
    key = "jqefTczMc7eaKLIu848AE5przJk1wVjw"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:

        
        resp = client.stocks_equities_daily_open_close("AAPL", "2021-05-15")
        print(f"On: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")


if __name__ == '__main__':
    main()