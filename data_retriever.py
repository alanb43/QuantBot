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

import requests
from bs4 import BeautifulSoup
import os

# REQUIRES: list of filenames to remove, the directory where they're stored
# EFFECTS: removes the files from the directory if they exist
def remove_files(file_list, storage_path = './'):
  for file in file_list:
    if os.path.exists(storage_path + file):
      os.remove(storage_path + file)

# REQUIRES: url formatted as string of website to scrape
# EFFECTS: returns BeautifulSoup object of sites html contents
def create_soup(url):
  response = requests.get(url)
  return BeautifulSoup(response.text, 'html.parser')

# REQUIRES: input file and output file to read / write from
#           ** THEY MUST ALREADY BE OPENED **
# EFFECTS: writes a single copy of each line to output file
def remove_duplicate_lines(input, output):
  lines_seen = set()
  line_num = 1
  for line in input:
    # skip past first 9 links because they're not stock specific
    if line not in lines_seen and line_num > 9:
      output.write(line)
      lines_seen.add(line)
    line_num += 1

# REQUIRES: a string representing a stock ticker
# EFFECTS: Accesses MarketWatch, searches the ticker's page for news articles,
#          finds, filters, and individualizes links to articles. Creates a file
#          containing links to all of the ticker's stories, returns its path.
def scrape_news_links(ticker):
  soup = create_soup(f'https://www.marketwatch.com/investing/stock/{ticker}?mod=quote_search')
  storage_path = 'data_retriever_storage/news/'
  paths = ['mw_a_tags.txt', 'mw_unrefined_links.txt', 'mw_links.txt']
  remove_files(paths, storage_path)

  # Where we'll store the <a> html elements
  all_a_tags = open(storage_path + paths[0], 'w')
  for a_tag in soup.findAll('a'):
    all_a_tags.write(str(a_tag))
  
  all_a_tags.close()
  all_a_tags = open(storage_path + paths[0], 'r')
  temp_links = open(storage_path + paths[1], 'w')
  # Many of the <a> elements have unwanted info or nested elements 
  for line in all_a_tags:
    # find link, check if it's to news story, add it to temp_links if so
    if line.find('href') != -1:
      link_start = line.find('href') + 6
      link_end = line.find('>', link_start)
      link = line[link_start: link_end - 1]
      if link[:34] == 'https://www.marketwatch.com/story/':
        temp_links.write(link + '\n')
      elif link[:37] == 'https://www.marketwatch.com/articles/':
        temp_links.write(link + '\n')

  temp_links.close()
  temp_links = open(storage_path + paths[1], 'r')
  final_links = open(storage_path + paths[2], 'w')
  remove_duplicate_lines(temp_links, final_links)
  final_links.close()

  return storage_path + paths[2]

scrape_news_links('aapl')




def scrape_news_data(url):
  soup = create_soup(url)
  #input = "/data_retriever_storage/news/mw_links.txt"
  file = open('input.txt', 'w')
  file.write(soup.get_text())
  input = 'input.txt'
  output = 'real_output.txt'
  file.close()
  file1 = open(input, 'r')
  file2 = open(output, 'w')
  remove_duplicate_lines(file1, file2)


# FOR LATER REFERENCE FOR USING DATETIME
# import time, datetime
# period1 = int(time.mktime(datetime.datetime(2018, 5, 22, 23, 59).timetuple()))
# period2 = int(time.mktime(datetime.datetime(2019, 5, 22, 23, 59).timetuple()))
