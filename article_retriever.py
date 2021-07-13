from datetime import date
import requests
from bs4 import BeautifulSoup
from models.article import Article

class ArticleRetriever:
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


  def __create_soup(self, url):
    '''
    REQUIRES: url formatted as string of website to scrape
    EFFECTS: returns BeautifulSoup object of sites html contents
    '''
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


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
    a_tag_list = []
    for a_tag in soup.findAll('a'):
      a_tag_list.append(str(a_tag))

    link_set = set()
    unrelated_links = 0
    # Many of the <a> elements have unwanted info or nested elements 
    for tag in a_tag_list:
      # find link, check if it's to news story, add it to temp_links if so
      if tag.find('href') != -1:
        link_start = tag.find('href') + 6
        link_end = tag.find('>', link_start)
        link = tag[link_start: link_end - 1]
        if link[:34] == self.STORY or link[:37] == self.ARTICLE:
          unrelated_links += 1
          if unrelated_links > 10:
            link_set.add(link)
    
    return link_set


  def scrape_news_data(self, url):
    '''
    REQUIRES: string of article link, int number associated with output
              file name, string ticker representing associated stock
    MODIFIES: technically modifies a file that we use to move desired text
              to our output file, but this file is deleted (end of func)
    EFFECTS:  Parses the entire article webpage's text for article info
              that we want, storing it in a file at the path.
    '''
    soup = self.__create_soup(url)
    article_html_contents = soup.get_text()
    advertisement_count = 0
    title_tag = str(soup.find("title"))
    title = title_tag[title_tag.index(">") + 1 : title_tag.rindex("-")]
    article_content = ""
    beginning_junk = True
    words_that_end = ["Editor's", "Read", "Read:", "read:", "Write", "Email"]
    for word in article_html_contents.split():
      if word == 'Advertisement':
        advertisement_count += 1
        continue
      if advertisement_count == 4:
        if beginning_junk:
          if (word.isalpha() and not word.isupper()):
            beginning_junk = False
        if not beginning_junk:
          if word in words_that_end:
            break
          article_content += word + " "
          if "Community Guidelines" in article_content or "performs" in title:
            return "BAD ARTICLE"

    article = Article(title, url, date.today(), article_content)
    return article


  # For website to display brief intro on mainpage
  def get_article_intro(self, article):
    '''
    REQUIRES: a valid path to a news article's contents
    EFFECTS:  returns a string of the first 45 relevant words in the article,
              as a brief intro to be used on the site
    '''
    intro = ""
    for word in article.contents.split()[:40]:
      intro += word + " "
    
    return intro


  # main function bot will use to gather articles for stocks
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
    links = self.__scrape_news_links(ticker)
    news_articles = []
    for link in links:
      article = self.scrape_news_data(link)
      if article != "BAD ARTICLE":
        news_articles.append(article)
    
    return news_articles

# from data_retriever import DataRetriever
# DR = DataRetriever()
# DR.get_article_intro("./data_retriever_storage/news/news_article_contents/TSLA/TSLA1.txt")
#'./data_retriever_storage/news/news_article_contents/