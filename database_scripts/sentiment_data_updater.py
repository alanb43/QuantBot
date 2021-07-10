import operator
from sqlite3.dbapi2 import IntegrityError
from nltk import FreqDist
import __init__
import queries
from config import *
from data_retriever import DataRetriever
import numpy as np

words = ["joshua", "profit", "loss", "annarbor", "bartSimpson", "fartSimpson"]

# To insert / read from Sentiment Data Table
#
#   word,
#   category,
#   positive_freq,
#   negative_freq,
#   frequency
#
# To update 
# 
#   positive_freq,
#   negative_freq
#   frequency
#   word


# How sentiments should be formatted EVERY STEP OF THE WAY
# Positive, Negative
# Category Options
# Semiconductors, Computer_Services, Production_Technology_Equipment, Software, Computer_Hardware


# UPDATE READ_IN, WRITE ISNT NEEDED
class SentAnalyzer():

  def __init__(self) -> None:
      self.num_articles = 0
      self.pos_articles = 0
      self.neg_articles = 0
      self.pos = {}
      self.neg = {}
      # Words determined to appear in high frequency with low value through training
      self.__words_to_skip = [
        'the', 'that', 'to', 'for', 'on', 'and', 'of', 'a', 'in', 'is', 'it', 'its', 'be', 'are',
        'has', 'than', 'by', 'man', 'he', 'she', 'from', 'an', 'with', 'about'
      ]


  def update_words_to_ditch(self, words_to_ditch):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__words_to_ditch += words_to_ditch

  # DETERMINE MEANS OF ACCESSING ARTICLE CONTENTS 
  # LIKELY ON AN ARTICLE TO ARTICLE BASIS BY SEARCHING DB FOR "ANALYZED " = 0


  def read_sentiment_data(self):
    self.pos = {}
    self.neg = {}
    self.num_articles = CURSOR.execute(queries.SELECT_TOTAL_NUM_ARTICLES).fetchone()[0]
    self.pos_articles = CURSOR.execute(queries.SELECT_POS_NUM_ARTICLES).fetchone()[0]
    self.neg_articles = CURSOR.execute(queries.SELECT_NEG_NUM_ARTICLES).fetchone()[0]

    CURSOR.execute(queries.SELECT_ALL_SENTIMENT_DATA)
    for row in CURSOR.fetchall():
      word, pos_freq, neg_freq = row["word"], row["positive_freq"], row["negative_freq"]
      self.pos[word] = pos_freq
      self.neg[word] = neg_freq


  def tokenize(self, article_content):
    '''
    REQUIRES: article content from SQL record
    EFFECTS:  returns list of words from the file (unrefined)
    '''
    return article_content.split()

  
  def remove_noise(self, tokens_list):
    '''
    REQUIRES: list representing unrefined words from article
    MODIFIES: removes noise from the tokens: removes punctuation, lowercase applied
              to all words, removes numbers (only maintains percentages), removes words
              that determined to be low-value + frequent (see __init__)
    EFFECTS:  returns list of cleaned / 'noise-less' tokens
    '''
    punctuation = '''#@,();:?/’|.\^=$”“''' # punctuation we choose to omit
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
      if token.isdigit() or len(token) > 12:
        continue
      if 'https' in token:
        continue 
      if token not in self.__words_to_skip:
        cleaned_tokens_list.append(token)
    
    return cleaned_tokens_list


  def create_master_dict(self):
    master = {**self.pos, **self.neg}
    for word in master.keys():
      if word in self.pos and word in self.neg:
        master[word] = self.pos[word] + self.neg[word]

    return master


  def bayes_calculation(self, cleaned_tokens, master):
    """
    Things needed to complete:
      1. total number of articles in entire training set: self.num_articles
      2. the number of unique words in the entire training set: make a master dictionary that adds frequencies if a word shows up in multiple dictionaries, get size
      3. for each word, the number of articles in the entire set that contain it: just the frequencies of the master dictionary
      4. for each category, number of articles with that label: self.pos_articles...
      5. for each category and word, number of articles with that category that have that word: original dictionaries
    """
    dictionaries = [self.pos, self.neg]
    # log_probabilities = {}
    # log_priors = [self.pos_articles / self.num_articles, self.neg_articles / self.num_articles]
    # articles = [self.pos_articles, self.neg_articles]
    # sentiments = ["Positive", "Negative"]
    # log_likelihood = 0
    # for word in cleaned_tokens:
    #   for dict in dictionaries:
    #     if dict.get(word):
    #       log_likelihood += np.log(dict[word] / articles[dictionaries.index(dict)])
    #     elif master.get(word):
    #       log_likelihood += np.log(master[word] / self.num_articles)
    #     else:
    #       log_likelihood += np.log(1 / self.num_articles)
    #     log_probability = np.log(log_priors[dictionaries.index(dict)])
    #     log_probabilities[sentiments[dictionaries.index(dict)]] = log_probability


    log_probabilities = {}
    log_priors = [self.pos_articles / self.num_articles, self.neg_articles / self.num_articles]
    print(log_priors)
    articles = [self.pos_articles, self.neg_articles]
    cats = ["Positive", "Negative"]
    for i in range(len(dictionaries)): #positive, negative
      log_likelihood = 0
      for word in cleaned_tokens: #words in article
        print(word + " is being iterated.")
        for y in range(len(dictionaries)):
          if dictionaries[y].get(word):
            log_likelihood += np.log(dictionaries[y][word] / articles[y])
          elif master.get(word):
            log_likelihood += np.log(master[word] / self.num_articles)
          else:
            log_likelihood += np.log(1 / self.num_articles)
            #print("LogLikelihood: ", log_likelihood, '\n')
      log_probability = np.log(log_priors[i]) + log_likelihood
      print("Log probability for ", cats[i], " dictionary: ", log_probability)
      log_probabilities[cats[i]] = log_probability

    maxCat = max(log_probabilities.items(), key=operator.itemgetter(1))[0]
    return [maxCat, log_probabilities[maxCat]]


  def update_database(self, freq_dist, category, sentiment):
    for word, freq in freq_dist.items():
      try:
        if sentiment == "Positive":
          CURSOR.execute(queries.INSERT_SENTIMENT_DATUM, (word, category, freq, 0, freq))
        else:
          CURSOR.execute(queries.INSERT_SENTIMENT_DATUM, (word, category, 0, freq, freq))
      except IntegrityError:
        # This is where we'd update the words' values
        CURSOR.execute(queries.SELECT_WORD_SENTIMENT_DATUM, (word,))
        content = CURSOR.fetchone()
        word, pos, neg, total = content["word"], content["positive_freq"], content["negative_freq"], content["frequency"]
        if sentiment == "Positive":
          positive = pos + freq
          total = positive + neg
          CURSOR.execute(queries.UPDATE_SENTIMENT, (positive, neg, total, word))
        else:
          negative = neg + freq
          total = negative + pos
          CURSOR.execute(queries.UPDATE_SENTIMENT, (pos, negative, total, word))
      finally:
        CONNECTION.commit()

  def analyze(self):
    # Loop through un-analyzed articles in DB. Analyze them, return answer about sentiment WITH CORRESPONDING STOCK.
    self.read_sentiment_data()
    print(self.pos_articles)
    CURSOR.execute(queries.SELECT_UNANALYZED_ARTICLES) # gets stock_id, article_content
    for row in CURSOR.fetchall():
      stock_id, article_content = row["stock_id"], row["article_content"]
      CURSOR.execute(queries.SELECT_STOCK_WITH_ID, (stock_id,))
      row = CURSOR.fetchone()
      stock_symbol, stock_category = row["symbol"], row["category"] # (ex) semiconductors
      token_list = self.tokenize(article_content)
      cleaned_token_list = self.remove_noise(token_list)
      freq_dist = FreqDist(cleaned_token_list)
      master_dict = self.create_master_dict()
      sentiment = self.bayes_calculation(cleaned_token_list, master_dict)
      self.update_database(freq_dist, stock_category, sentiment)
  

  def model_trainer(self, stock_id, sentiment, category, url):
    DR = DataRetriever()
    article = DR.scrape_news_data(url) # returns Article object
    tokens = self.tokenize(article.contents)
    cleaned_tokens = self.remove_noise(tokens)
    freq_dist = FreqDist(cleaned_tokens)
    self.update_database(freq_dist, category, sentiment)
    CURSOR.execute(queries.INSERT_NEWS_ARTICLE, (stock_id, article.title, article.date, url, 1, sentiment, article.contents))
    CONNECTION.commit()

SA = SentAnalyzer()
SA.model_trainer(23, "Negative", "Semiconductors", "https://www.marketwatch.com/story/another-intel-product-delay-drags-chip-stocks-dow-lower-11624987740?mod=mw_quote_news")
SA.model_trainer(23, "Negative", "Semiconductors", "https://www.marketwatch.com/articles/intel-chips-semiconductors-notebook-sales-production-51624293623?mod=mw_quote_news_seemore")


