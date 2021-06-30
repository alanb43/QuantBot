from enum import Enum

class TimeFrame(Enum):
  '''
  For use with alpaca API. Required for get_bars API call.
  '''
  Day = "1Day"
  Hour = "1Hour"
  Minute = "1Min"
  Sec = "1Sec"
