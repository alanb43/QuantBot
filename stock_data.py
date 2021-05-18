import time

from polygon import WebSocketClient, STOCKS_CLUSTER

def process_message(message):
  print("process message", message)

def main():
  key = 'jqefTczMc7eaKLIu848AE5przJk1wVjw'
  my_client = WebSocketClient(STOCKS_CLUSTER, key, process_message)
  my_client.run_async()

  my_client.subscribe("T.AAPL")
  time.sleep(1)

  my_client.close_connection()

if __name__ == "__main__":
  main()