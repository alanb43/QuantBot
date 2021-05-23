import urllib.request
import time

# REQUIRES: string representing stock symbol in CAPS (ex : 'TSLA'), string
#           representing a time range in this format : #w, #m, #y where # is
#           the number of weeks, months, or years of data you want leading up
#           to today's data.
# EFFECTS:  obtains the stock's price history from today to today minus the
#           entered timerange and stores it in a csv file on the repo.
# EXAMPLES OF TIME RANGES: '1w' '2y' '6m' 
def get_prices(ticker, time_range, interval = '1d'): 
  path = 'data_retriever_storage/prices'
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
  download_url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
  download_path = f'./{path}/{ticker}_prices.csv'
  urllib.request.urlretrieve(download_url, download_path)

get_prices('AAPL', '1y')
#################################################################
#                                                               #
#             FOR WEB SCRAPING NEWS ARTICLES:                   #
#      this simple script/function retreives all of the         #
#      financial news stories from marketwatch when used.       #
#      It stores them in data_retriever_storage/, and also      #
#      returns this path for the bot's later use.               #
#                                                               #
#################################################################

import requests
from bs4 import BeautifulSoup
import os

def scrape_news():
  # Get the URL and create BeautifulSoup object with its contents
  url = 'https://www.marketwatch.com/'
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  storage_path = 'data_retriever_storage/news/'
  # Remove the last links present for fresh data (might be overkill)
  if os.path.exists(storage_path + "mw_a_tags.txt"):
    os.remove(storage_path + "mw_a_tags.txt")
  if os.path.exists(storage_path + "mw_unrefined_links.txt"):
    os.remove(storage_path + "mw_links.txt")
  
  # Where we'll store the <a> html elements
  all_a_tags = open(storage_path + 'mw_a_tags.txt', 'w')

  for a_tag in soup.findAll('a'):
    all_a_tags.write(str(a_tag))

  all_a_tags.close()
  all_a_tags = open(storage_path + 'mw_a_tags.txt', 'r')
  temp_links = open(storage_path + 'mw_unrefined_links.txt', 'w')
  # Now we read through the <a> elements. A lot of them contains unwanted
  # nested elements, as well as unuseful info (class, id, style, etc)
  for line in all_a_tags:
    # we determine if the if the link is to a story, and add it to temp_links
    if line.find('href') != -1:
      link_start = line.find('href') + 6
      link_end = line.find('>', link_start)
      link = line[link_start: link_end - 1]
      if link[:34] == 'https://www.marketwatch.com/story/':
        temp_links.write(link + '\n')

  temp_links.close()
  temp_links = open(storage_path + 'mw_unrefined_links.txt', 'r')
  final_links = open(storage_path + 'mw_links.txt', 'w')
  # I would've ended here, however the site has a LOT of duplicate links. Now
  # we'll remove all of the duplicates and finally store the final links
  lines_seen = set()
  
  for line in temp_links:
    if line not in lines_seen:
      final_links.write(line)
      lines_seen.add(line)
  
  final_links.close()

  path_to_good_links = storage_path + 'mw_links.txt'
  return path_to_good_links

scrape_news()

# FOR LATER REFERENCE FOR USING DATETIME
# import time, datetime
# period1 = int(time.mktime(datetime.datetime(2018, 5, 22, 23, 59).timetuple()))
# period2 = int(time.mktime(datetime.datetime(2019, 5, 22, 23, 59).timetuple()))
