import urllib.request
import time
import requests
from bs4 import BeautifulSoup
import os

class DataRetriever:
  '''

  Data Retrieval tool for both price history and stock news, utilizing yahoo
  finance and MarketWatch for the respective subjects. May be updated to include
  more financial data in the near future.

  0. Init
  1. Simple Helper Functions
  2. Scraping/Implementation Helpers
  3. Functions the Bot should use / access 

  NOTE: Helper functions start with '__' to make them private to the class
        Create an instance : DR = DataRetriever(), use this instance to call
        functions many times.

  '''

  def __init__(self) -> None:
    return


  ''' 1. Simple Helper Functions '''


  def __remove_files(self, file_list, path = './') -> None:
    '''
    REQUIRES: list of filenames to remove, the directory where they're stored
    EFFECTS: removes the files from the directory if they exist
    '''
    for file in file_list:
      if os.path.exists(path + file):
        os.remove(path + file)


  def __create_soup(self, url):
    '''
    REQUIRES: url formatted as string of website to scrape
    EFFECTS: returns BeautifulSoup object of sites html contents
    '''
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

  
  def __remove_duplicate_lines(self, input, output, path):
    '''
    REQUIRES: input file name and output file name to read / write 
              from, path at which they're located   
    EFFECTS: writes a single copy of each line to output file
    '''
    lines_seen = set()
    line_num = 1
    file_in = open(path + input, 'r')
    file_out = open(path + output, 'w')
    for line in file_in:
      # (MW specific) skip past first 9 links because they're not related
      if line not in lines_seen and line_num > 9:
        file_out.write(line)
        lines_seen.add(line)
      line_num += 1

    file_out.close()


  ''' 2. Scraping/Implementation Helpers'''


  def __scrape_news_links(self, ticker):
    '''
    REQUIRES: a string representing a stock ticker
    MODIFIES: technically modifies files that we use to grab desired links
              to our output file, but this file is deleted (end of func)
    EFFECTS: Accesses MarketWatch, searches the ticker's page for news articles,
            finds, filters, and individualizes links to articles. Creates a file
            containing links to all of the ticker's stories, returns its path.
    '''
    soup = self.__create_soup(f'https://www.marketwatch.com/investing/stock/{ticker}?mod=quote_search')
    path = 'data_retriever_storage/news/news_links/'
    files = ['mw_a_tags.txt', 'mw_unrefined_links.txt', f'mw_{ticker}_links.txt']
    self.__remove_files(files, path)

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
    self.__remove_duplicate_lines(files[1], files[2], path)
    files_to_remove = [files[0], files[1]]
    self.__remove_files(files_to_remove, path)


  def __scrape_news_data(self, url, article_num, ticker):
    '''
    REQUIRES: string of article link, int number associated with output
              file name, string ticker representing associated stock
    MODIFIES: technically modifies a file that we use to move desired text
              to our output file, but this file is deleted (end of func)
    EFFECTS:  Parses the entire article webpage's text for article info
              that we want, storing it in a file at the path.
    '''
    soup = self.__create_soup(url)
    pathname = f'./data_retriever_storage/news/news_article_contents/{ticker}/'
    if not os.path.exists(pathname):
      os.mkdir(pathname)
    input = url[37:url.rfind('-')]
    file = open(pathname + input, 'w')
    file.write(soup.get_text())
    output = ticker + str(article_num) + '.txt'
    file.close()
    file = open(pathname + input, 'r')
    file1 = open(pathname + output, 'w')
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
    self.__remove_files([input], pathname)


  ''' 3. Functions the Bot should use / access'''
  
  
  def get_stock_prices(self, ticker, time_range, interval = '1d'):
    '''
    REQUIRES: string representing stock symbol in CAPS (ex : 'TSLA'), string
          representing a time range in this format : #w, #m, #y where # is
          the number of weeks, months, or years of data you want leading up
          to today's data.
    EFFECTS:  obtains the stock's price history from today to today minus the
              entered timerange and stores it in a csv file on the repo.
    EXAMPLES OF TIME RANGES: '1w' '2y' '6m' 
    '''
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


  def get_stock_news(self, ticker):
    '''
    REQUIRES: a string representing a valid ticker / symbol
    MODIFIES: news folder's subfolders (populates them)
    EFFECTS: gathers news links related to a ticker, parses through
            each link for article content, stores individual contents
            in numbered files.
    NOTE: at some point the deletion of past stock news should be added
          before the new article contents are stored, as well as the 
          updating of paths to reflect individual tickers for sorting and 
          storage simplicity.
    '''
    self.__scrape_news_links(ticker)
    path = './data_retriever_storage/news/news_links/'
    if os.path.exists(path + f'mw_{ticker}_links.txt'):
      links_file = open(path + f'mw_{ticker}_links.txt')
    else:
      return "Links haven't been scraped. Use scrape_news_links"
    link_number = 1
    for link in links_file:
      self.__scrape_news_data(link, link_number, ticker)
      link_number += 1

''' Example '''
DR = DataRetriever()
DR.get_stock_news('AAPL')
DR.get_stock_prices('NHI', '1y')