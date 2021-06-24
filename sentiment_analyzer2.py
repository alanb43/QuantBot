from nltk import FreqDist
import os
import requests
from bs4 import BeautifulSoup
from data_retriever import DataRetriever
import numpy as np
import operator

class SentimentAnalyzer:

  def __init__(self) -> None:
    # Initialize counters for number of (pos & neg & overall) articles, dictionaries 
    self.num_articles = 0
    self.pos_dict = {}
    self.pos_articles = 0
    self.neg_dict = {}
    self.neg_articles = 0
    # Words determined to appear in high frequency with low value through training
    self.__words_to_skip = [
      'the', 'that', 'to', 'for', 'on', 'and', 'of', 'a', 'in', 'is', 'it', 'its', 'be', 'are',
      'has', 'than', 'by', 'man', 'he', 'she', 'from', 'an', 'with', 'about'
    ]


  def __articles_and_count(self, ticker):
    '''
    EFFECTS: returns a list of the article filenames for the given ticker
             and the number of articles.
    '''
    path = f'data_retriever_storage/news/news_article_contents/{ticker}/'
    article_list = os.listdir(path)
    return (article_list, len(article_list))


  def update_words_to_ditch(self, words_to_ditch):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__words_to_ditch += words_to_ditch


  def __tokenize(self, path):
    '''
    REQUIRES: str representing valid path (filename included!) to article data file
    EFFECTS:  creates, populates, and returns list of words from the file (unrefined)
    '''
    file = open(path, 'r')
    keep_skipping = True
    tokens_list = []
    for line in file:
      if len(line.split()) > 2:
        keep_skipping = False
      if keep_skipping or len(line.split()) == 0:
        continue
      tokens = list(line.split())
      tokens_list += tokens
    
    return tokens_list

  
  def __remove_noise(self, tokens_list):
    '''
    REQUIRES: list representing unrefined words from article
    MODIFIES: removes noise from the tokens: removes punctuation, lowercase applied
              to all words, removes numbers (only maintains percentages), removes words
              that determined to be low-value + frequent (see __init__)
    EFFECTS:  returns list of cleaned / 'noise-less' tokens
    '''
    punctuation = '''#@,();:?/’|.\^$”“''' # punctuation we choose to omit
    cleaned_tokens_list = []
    for token in tokens_list:
      if '$' in token or token.isdigit() or token[0] == '-' or token[0] == '—':
        continue
      if '%' not in token: # if it's not a percentage
        token = token.lower()
        if "’s" in token:
          token = token.replace("’s", "")
        elif "'s" in token:
          token = token.replace("'s", "")
      for ch in token:
        if ch in punctuation:
          token = token.replace(ch, "")
      if token.isdigit():
        continue
      if token not in self.__words_to_ditch:
        cleaned_tokens_list.append(token)
    
    return cleaned_tokens_list

  
  def get_all_words(self, cleaned_tokens_list):
    ''' 
    REQUIRES: list containing tokens that already have noised removed from them
    EFFECTS:  yields each token 
    '''
    for tokens in cleaned_tokens_list:
      for token in tokens:
        yield token


  def __read_in_freq_dict(self, ticker):
    path = f"data_retriever_storage/news/sentiment_data/{ticker}_sentiment_data.txt"
    if not os.path.exists(path):
      return
    with open(path, 'r') as f:
      lines = f.readlines()
      if len(lines) == 0:
        return None
      self.num_articles = int(lines[0])
      article_nums = [self.pos_articles, self.neg_articles]
      article_dicts = [self.pos_dict, self.neg_dict]
      tracker = 0
      for line in lines[1:]:
        if line == "\n":
          tracker += 1 # file has positive / negative data separated by blank lines
        line_split = line.split()
        if len(line_split) < 2:
          if len(line_split) == 1 and line_split[0].isdigit():
            article_nums[tracker] = int(line_split[0])
        else:
          article_dicts[tracker][line_split[0]] = int(line_split[1])
      
      self.pos_articles = article_nums[0]
      self.neg_articles = article_nums[1]
    

  def __write_to_freq_dict(self, ticker):
    path = f"data_retriever_storage/news/sentiment_data/{ticker}_sentiment_data.txt"
    f = open(path, 'w')
    f.write(str(self.num_articles) + "\n")
    f.write("Positive\n")
    f.write(str(self.pos_articles) + "\n")
    for key in self.pos_dict.keys():
      line = key + " " + str(self.pos_dict[key]) + "\n"
      f.write(line)
    f.write("\n")
    f.write("Negative\n")
    f.write(str(self.neg_articles) + "\n")
    for key in self.neg_dict.keys():
      line = key + " " + str(self.neg_dict[key]) + "\n"
      f.write(line)


  def buy_sell_decider(self, ticker, filepath, category):
    if category[0] == "Positive":
      action = "Buy"
    elif category[0] == "Negative":
      action = "Sell"
    else: # not doing either
      return None

    quantity = 0
    if category[1] > 100:
      quantity = 1
    elif category[1] > 1000:
      quantity = 2
    # .... idk what these values should be we need to talk about that they're probably going to be percentages of how much we own in that company

    with open(filepath, 'r') as f_in:
      article_name = f_in.readline()
      url = f_in.readline()
    
    DR = DataRetriever()
    with open('./models/decisions.txt', 'a') as f_out:
      f_out.write(ticker + "\n")
      f_out.write(action + "\n")
      f_out.write(str(quantity) + "\n")
      f_out.write(article_name)
      f_out.write(url)
      f_out.write(DR.get_article_intro(filepath) + "\n")
    
    print("The article: '" + article_name + "' has led QuantBot to " + action + " " + str(quantity) + " shares of " + ticker + ".\n")
  

  def __update_freq_dict(self, freq_dist, freq_dict, category = [], filepath = ""):
    for key in freq_dist:
      freq = freq_dist.get(key)
      if key in freq_dict.keys():
        freq_dict[key] += int(freq) - 1
      else:
        freq_dict[key] = 1
    if filepath != "":
      self.buy_sell_decider(filepath, category)
  

  def model_trainer(self, ticker, type, url):
    self.__read_in_freq_dict()
    path = f"data_retriever_storage/news/sentiment_data/"
    DR = DataRetriever()
    DR.training_data_scraper(url, ticker, path)
    tokens_list = self.__tokenize(path + f"{ticker}_train_out.txt")
    cleaned_tokens_list, mentions = self.__remove_noise(tokens_list)
    all_words = self.get_all_words(cleaned_tokens_list)
    freq_dist = FreqDist(all_words)
    self.num_articles += 1
    if type == "positive":
      self.__update_freq_dict(freq_dist, self.pos_dict)
      self.pos_articles += 1 
    elif type == "negative":
      self.__update_freq_dict(freq_dist, self.neg_dict)
      self.neg_articles += 1
    self.__write_to_freq_dict()
    if os.path.exists(path + f"{ticker}_train_out.txt"):
      os.remove(path + f"{ticker}_train_out.txt")
      os.remove(path + f"{ticker}_train.txt")


  def bayes_calculation(self, words):
    """
    Things needed to complete:
      1. total number of articles in entire training set: self.num_articles
      2. the number of unique words in the entire training set: make a master dictionary that adds frequencies if a word shows up in multiple dictionaries, get size
      3. for each word, the number of articles in the entire set that contain it: just the frequencies of the master dictionary
      4. for each category, number of articles with that label: self.pos_articles...
      5. for each category and word, number of articles with that category that have that word: original dictionaries
    """
    dictionaries = [self.pos_dict, self.neg_dict]
    master = {}
    for dict in dictionaries:
      for word in dict.keys():
        if master.get(word):
          master[word] += dict[word]
        else:
          master[word] = 1  

    log_probabilities = {}
    log_priors = [self.pos_articles / self.num_articles, self.neg_articles / self.num_articles]
    articles = [self.pos_articles, self.neg_articles]
    cats = ["Positive", "Negative"]
    for i in range(len(dictionaries)):
      log_likelihood = 0
      for word in words:
        for y in range(len(dictionaries)):
          if dictionaries[y][word]:
            log_likelihood += np.log(dictionaries[y][word] / articles[y])
          elif master[word]:
            log_likelihood += np.log(master[word] / self.num_articles)
          else:
            log_likelihood += np.log(1 / self.num_articles)
          y += 1
      log_probability = np.log(log_priors[i]) + log_likelihood
      log_probabilities[cats[i]] = log_probability
      i += 1
    maxCat = max(log_probabilities.items(), key=operator.itemgetter(1))[0]
    return [maxCat, log_probabilities[maxCat]]


  def analyze(self, ticker):
    self.__read_in_freq_dict()
    num, article_files = self.__articles_and_count(ticker)
    self.num_articles += int(num)
    for file_name in article_files:
      file_path = f"data_retriever_storage/news/news_article_contents/{ticker}/{file_name}"
      tokens_list = self.__tokenize(file_path)
      cleaned_tokens_list = self.__remove_noise(tokens_list)
      all_words = self.get_all_words(cleaned_tokens_list)
      freq_dist = FreqDist(all_words) # maps word to freq
      category = self.bayes_calculation(all_words)
      if category[0] == "Positive": 
        self.__update_freq_dict(freq_dist, self.pos_dict, category, file_path)
        self.pos_articles += 1
      else: 
        self.__update_freq_dict(freq_dist, self.neg_dict, category, file_path)
        self.neg_articles += 1
    
    self.__write_to_freq_dict()


    '''
    def testing_dicts(self):
      self.__read_in_freq_dict()
    '''


# SA = SentimentAnalyzer()
# SA.analyze('TSLA')
# SA.model_trainer('TSLA', 'negative' 'https://www.marketwatch.com/story/suze-orman-says-bitcoin-is-a-place-to-put-some-money-and-just-leave-it-11623703566?mod=mw_quote_news')
    
# analyze returns [Strong sell, light sell, nothing, light buy, Strong buy]
# Strong sell dumps 75% - 100% depending time series
# 