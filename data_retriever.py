import urllib.request
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os, shutil

class DataRetriever:
  '''
  
  Data Retrieval tool for both price history and stock news, utilizing yahoo
  finance and MarketWatch for the respective subjects. May be updated to include
  more financial data in the near future.

  1. Simple Helper Functions
  2. Scraping/Implementation Helpers
  3. Functions the Bot should use / access 

  NOTE: Helper functions start with '__' to make them private to the class
  NOTE: Create an instance : DR = DataRetriever(), use this instance to call
        functions many times.

  '''


  def __init__(self) -> None:
    self.STORY = 'https://www.marketwatch.com/story/'
    self.ARTICLE = 'https://www.marketwatch.com/articles/'
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
    file_out = open(path + output, 'a')
    for line in file_in:
      # (MW specific) skip past first 9 links because they're not related
      if line not in lines_seen and line_num > 9:
        file_out.write(line)
        lines_seen.add(line)
      line_num += 1

    file_out.close()

  ''' 2. Scraping/Implementation Helpers'''

  def __get_timestamp(self, news_soup):
    dt = str(news_soup.find('time', class_='timestamp timestamp--pub'))
    dt = dt[dt.find(": ") + 2: dt.find(" at")]
    dt = dt[dt.index(' ') + 1: dt.index(',')] + ' ' + dt[:dt.index(' ')] + ',' + dt[dt.rindex(' '):]
    d8time = datetime.strptime(dt, "%d %B, %Y")
    return d8time
    

  def __compare_timestamp(self, ticker, timestamp) -> bool:
    path = f"./data_retriever_storage/news/sentiment_data/{ticker}_sentiment_data.txt"
    sentiment_data = open(path, 'r')
    sentiment_data.readline()
    latest_timestamp = sentiment_data.readline()
    if timestamp > latest_timestamp:
      return True
    return False

  def __compare_links(self, soup, path, files):
    a_tags = []
    duplicate_links = []
    for a_tag in soup.findAll('a'):
      a_tags.append(str(a_tag))
    for tag in a_tags:
      if tag.find('href') != -1:
        link_start = tag.find('href') + 6
        link_end = tag.find('>', link_start)
        link = tag[link_start: link_end - 1]
        if link[:34] == self.STORY or link[:37] == self.ARTICLE:
          for old_link in open(path + files[2], 'r'):
            if link == old_link[:-1]:
              duplicate_links.append(link)
    
    return duplicate_links


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
    #links_to_ignore = self.__compare_links(soup, path, files)
    self.__remove_files(files, path)
    pathname = f'./data_retriever_storage/news/news_article_contents/{ticker}/'
    if os.path.exists(pathname):
      shutil.rmtree(pathname)
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
        if link[:34] == self.STORY or link[:37] == self.ARTICLE:
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
    title_tag = str(soup.find("title"))
    title = title_tag[title_tag.index(">") + 1 : title_tag.rindex("-")]
    file1.write(title + '\n')
    file1.write(url)
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
    file1 = open(pathname + output, 'r')
    remove = [input]
    if len(file1.readlines()) < 7:
      remove.append(output)
    file1.close()
    self.__remove_files(remove, pathname)


  def get_article_intro(self, path):
    '''
    REQUIRES: a valid path to a news article's contents
    EFFECTS:  returns a string of the first 45 relevant words in the article,
              as a brief intro to be used on the site
    '''
    article_words = []
    with open(path, 'r') as file:
      file.readline()
      line = file.readline()
      while len(line.split()) < 3:
        line = file.readline()
      
      article_words += line.split()
      while len(article_words) < 40:
        article_words += file.readline().split()

      intro_string = ""
      word_count = 0
      for word in article_words:
        if word_count == 45:
          break
        intro_string += word + " "
        word_count += 1
      
      return intro_string
      

  def training_data_scraper(self, url, ticker, path):
    soup = self.__create_soup(url)
    file = open(path + ticker + '_train.txt', 'w')
    file.write(soup.get_text())
    output = ticker + '_train_out.txt'
    file.close()
    file = open(path + ticker + '_train.txt', 'r')
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
    file1 = open(path + output, 'r')
    remove = []
    if len(file1.readlines()) < 7:
      remove.append(output)
    file1.close()


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
    if time_range[-1] == 'w':
      period = int(time_range[:-1]) * int(31536000 / 52)
    elif time_range[-1] == 'm':
      period = int(time_range[:-1]) * int(31536000 / 12)
    elif time_range[-1] == 'y':
      period = int(time_range[:-1]) * 31536000
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
    path = f'./data_retriever_storage/news/news_links/mw_{ticker}_links.txt'
    #sent_path = f'./data_retriever_storage/news/sentiment_data/{ticker}_sentiment_data.txt'
      # need to create system where links are not reread from file
    links_file = open(path, 'r')
    link_number = 1
    for link in links_file:
      self.__scrape_news_data(link, link_number, ticker)
      link_number += 1

DR = DataRetriever()
DR.get_stock_news("AAPL")

# from data_retriever import DataRetriever
# DR = DataRetriever()
# DR.get_article_intro("./data_retriever_storage/news/news_article_contents/TSLA/TSLA1.txt")
#'./data_retriever_storage/news/news_article_contents/