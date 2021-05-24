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

#get_prices('AAPL', '1y')

import requests
from bs4 import BeautifulSoup
import os

# REQUIRES: list of filenames to remove, the directory where they're stored
# EFFECTS: removes the files from the directory if they exist
def remove_files(file_list, path = './'):
  for file in file_list:
    if os.path.exists(path + file):
      os.remove(path + file)

# REQUIRES: url formatted as string of website to scrape
# EFFECTS: returns BeautifulSoup object of sites html contents
def create_soup(url):
  response = requests.get(url)
  return BeautifulSoup(response.text, 'html.parser')

# REQUIRES: input file name and output file name to read / write 
#           from, path at which they're located
#           
# EFFECTS: writes a single copy of each line to output file
def remove_duplicate_lines(input, output, path):
  lines_seen = set()
  line_num = 1
  file_in = open(path + input, 'r')
  file_out = open(path + output, 'w')
  for line in file_in:
    # skip past first 9 links because they're not stock specific
    if line not in lines_seen and line_num > 9:
      file_out.write(line)
      lines_seen.add(line)
    line_num += 1

  file_out.close()


# REQUIRES: a string representing a stock ticker
# EFFECTS: Accesses MarketWatch, searches the ticker's page for news articles,
#          finds, filters, and individualizes links to articles. Creates a file
#          containing links to all of the ticker's stories, returns its path.
def scrape_news_links(ticker):
  soup = create_soup(f'https://www.marketwatch.com/investing/stock/{ticker}?mod=quote_search')
  path = 'data_retriever_storage/news/news_links/'
  files = ['mw_a_tags.txt', 'mw_unrefined_links.txt', f'mw_{ticker}_links.txt']
  remove_files(files, path)

  # Where we'll store the <a> html elements
  all_a_tags = open(path + files[0], 'w')
  for a_tag in soup.findAll('a'):
    all_a_tags.write(str(a_tag))
  
  all_a_tags.close()
  all_a_tags = open(path + files[0], 'r')
  temp_links = open(path + files[1], 'w')
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
  remove_duplicate_lines(files[1], files[2], path)
  files_to_remove = [files[0], files[1]]
  remove_files(files_to_remove, path)
  
  return path + files[2]

scrape_news_links('tsla')


def scrape_news_data(url, article_num, ticker):
  soup = create_soup(url)
  path = './data_retriever_storage/news/news_article_contents/'
  input = url[37:url.rfind('-')]
  file = open(path + input, 'w')
  file.write(soup.get_text())
  output = ticker + str(article_num) + '.txt'
  file.close()
  file = open(path + input, 'r')
  file1 = open(path + output, 'w')
  line_num, advertisement_count = 0, 0
  for line in file:
    line_num += 1
    if line == 'Advertisement\n':
      advertisement_count += 1
      continue
    if line != '\n' and advertisement_count == 4:
      if line[:9] == 'Read Next':
        break
      file1.write(line)

  file1.close()
  remove_files([input], path)


scrape_news_data('https://www.marketwatch.com/articles/ford-stock-electric-f150-lightning-launch-tesla-51621516206?mod=mw_quote_news', 1, 'tsla')
scrape_news_data('https://www.marketwatch.com/articles/ford-ev-f-150-lightning-orders-rush-in-the-stock-is-rising-51621606918?mod=mw_quote_news', 2, 'tsla')
scrape_news_data('https://www.marketwatch.com/articles/tesla-stock--price-outlook-hold-rating-51621866627?mod=mw_quote_news', 3, 'tsla')

# FOR LATER REFERENCE FOR USING DATETIME
# import time, datetime
# period1 = int(time.mktime(datetime.datetime(2018, 5, 22, 23, 59).timetuple()))
# period2 = int(time.mktime(datetime.datetime(2019, 5, 22, 23, 59).timetuple()))
