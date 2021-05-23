import urllib.request
import time

# REQUIRES: string representing stock / crypto in CAPS (ex : 'TSLA'), string
#           representing a time range in this format : #w, #m, #y where # is
#           the number of weeks, months, or years of data you want leading up
#           to today's data.
# EFFECTS:  obtains the stock's price history from today to today minus the
#           entered timerange and stores it in a csv file on the repo.
# EXAMPLES OF TIME RANGES: '1w' '2y' '6m' 
def get_prices(ticker, time_range): 
  if time_range[1] == 'w':
    period = int(time_range[0]) * int(31536000 / 52)
  elif time_range[1] == 'm':
    period = int(time_range[0]) * int(31536000 / 12)
  elif time_range[1] == 'y':
    period = int(time_range[0]) * 31536000
  else:
    return "ERROR: Invalid time_range entered. See examples"
  period2 = int(time.time())
  period1 = period2 - period
  download_url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
  download_path = f'./{ticker}_{time_range}_prices.csv'
  urllib.request.urlretrieve(download_url, download_path)



# FOR LATER REFERENCE FOR USING DATETIME
# import time, datetime
# period1 = int(time.mktime(datetime.datetime(2018, 5, 22, 23, 59).timetuple()))
# period2 = int(time.mktime(datetime.datetime(2019, 5, 22, 23, 59).timetuple()))



##########################################################
#                                                        #
#   FOR WEB SCRAPE (NOT NECESSARY FOR THIS)              #
#      moved from scraping because websites hid          #
#      links too deep for BeautifulSoup to detect        #
#                                                        #
##########################################################

#import requests
#from bs4 import BeautifulSoup
#from requests.api import get
#
# # URL we want to scrape data from
# url = 'http://web.mta.info/developers/turnstile.html'

# # We connect to the URL (response code 200 desired)
# response = requests.get(url)

# # We parse the HTML and save it to a BeautifulSoup object
# soup = BeautifulSoup(response.text, "html.parser")

# # To download the whole data set, let's do a for loop through all a tags
# line_count = 1 #variable to track what line you are on
# for one_a_tag in soup.findAll('a'):  #'a' tags are for links
#     if line_count >= 38: #code for text files starts at line 36
#         link = one_a_tag['href']
#         download_url = 'http://web.mta.info/developers/'+ link
#         urllib.request.urlretrieve(download_url,'./'+link[link.find('/turnstile_')+1:]) 
#         time.sleep(1) #pause the code for a sec
#     #add 1 for next line
#     line_count +=1