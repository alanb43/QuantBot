from nltk import FreqDist
import os


class SentimentAnalyzer:
  '''
  Class should support
    tokenizing
    removing noise
    determining density
    the actual model
    testing the model
  
    RIGHT NOW WE INITIALIZE:
      initialize with a ticker
      we tokenize from a file,
      and remove the noise from the tokens.

      need to build dataset and find prices after articles come out
      to determine positive / negative effects of article sentiments / words
  '''
  def __init__(self, ticker) -> None:
    self.__ticker = ticker
    self.__path = f'data_retriever_storage/news/news_article_contents/{ticker}/'
    self.__tickers = {
      'AAPL' : ['aapl', 'apple', 'tim', 'cook', 'iphone'], 
      'AMZN' : ['amzn', 'amazon', 'jeff', 'bezos'], 
      'TSLA' : ['tsla', 'elon', 'tesla', 'roadster', 'musk', 'meme', 'doge']
    }


  def __number_of_articles(self): 
    '''
    EFFECTS: returns the number of articles for the ticker the class object is 
             instantiated with, as well as a list of the filenames
    '''
    list = os.listdir(self.__path)
    return (len(list), list)


  def update_tickers(self, ticker, common_phrases):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__tickers[ticker] = common_phrases


  def __tokenize(self, path):
    '''
    REQUIRES: str representing valid path (filename included!) to article data file,
    EFFECTS:  creates, populates, and returns list of words from the file (unrefined)
    '''
    file = open(path, 'r')
    keep_skipping = True
    words = []
    for line in file:
      if len(line.split()) > 2:
        keep_skipping = False
      if keep_skipping or len(line.split()) == 0:
        continue
      a = list(line.split())
      words += a
    return words

  def __remove_noise(self, words, ticker):
    '''
    REQUIRES: list representing unrefined words from article, string (ALL CAPS) 
              representing ticker
    MODIFIES: tokenizes the data. removes punctuation, makes all words lowercase,
              maintains percentages, removes numbers if not part of a percentage,
              removes words that don't add anything (determined these words by 
              analyzing AAPL, AMZN, and TSLA articles for words excessively used)
    EFFECTS:  returns tuple containing tokenized words and the number of mentions
              of the desired ticker
    '''
    punctuation = '''#@,();:?/-|—.\^$'''
    mentions = 0
    words_to_ditch = ['the', 'that', 'to', 'for', 'on', 'and', 'of', 'a', 'in', 'is']
    newWords = []
    for word in words:
      word = word.lower()
      if '%' not in word: # if it's not a percentage
        if "’s" in word:
          word = word.replace("’s", "")
        elif "'s" in word:
          word = word.replace("'s", "")
        for ch in word:
          if ch in punctuation:
            word = word.replace(ch, "")
        if word.isdigit(): # non percentage related nums are ignored
          continue
      if word in self.__tickers[ticker]:
        mentions += 1
      if word not in words_to_ditch:
        newWords.append(word)
    return (newWords, mentions)

