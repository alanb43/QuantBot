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
    self.__words_to_ditch = [
      'the', 'that', 'to', 'for', 'on', 'and', 'of', 'a', 'in', 'is', 'it', 'its', 'be', 'are',
      'has', 'than', 'by', 'man', 'he', 'she', 'from', 'an', 'with', 'about'
    ]
    self.__tickers = {
      'AAPL' : ['aapl', 'apple', 'tim', 'cook', 'iphone'], 
      'AMZN' : ['amzn', 'amazon', 'jeff', 'bezos', 'delivery', 'space'], 
      'TSLA' : ['tsla', 'elon', 'tesla', 'roadster', 'musk', 'meme', 'doge', 'electric', 'model']
    }
    self.freq_dict = {}
    self.num_articles = 0

  def __number_of_articles(self): 
    '''
    EFFECTS: returns the number of articles for the ticker the class object is 
             instantiated with, as well as a list of the filenames
    '''
    list = os.listdir(self.__path)
    return (len(list), list)


  def update_tickers(self, common_phrases):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__tickers[self.__ticker] += common_phrases


  def update_words_to_ditch(self, words_to_ditch):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__words_to_ditch += words_to_ditch


  def __tokenize(self, path):
    '''
    REQUIRES: str representing valid path (filename included!) to article data file,
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
      tokens_list.append(tokens)
    return tokens_list


  def __remove_noise(self, tokens_list):
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
    punctuation = '''#@,();:?/’|.\^$”“'''
    mentions = 0
    cleaned_tokens_list = []
    for tokens in tokens_list:
      cleaned_tokens = []
      for token in tokens:
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
        if token in self.__tickers[self.__ticker]:
          mentions += 1
        if token not in self.__words_to_ditch:
          cleaned_tokens.append(token)
      cleaned_tokens_list.append(cleaned_tokens)
    return (cleaned_tokens_list, mentions)

  def get_all_words(self, cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
      for token in tokens:
        yield token

  def __read_in_freq_dict(self):
    path = f"data_retriever_storage/news/sentiment_data/{self.__ticker}_sentiment_data.txt"
    with open(path, 'r') as f:
      potential_num_files = f.readline() # come back when doing math
      if len(potential_num_files):
        self.num_articles = int(potential_num_files)
      else:
        self.num_articles = 0
      
      Lines = f.readlines()
      for line in Lines:
        line_split = line.split()
        if len(line_split) < 2:
          pass
        else:
          self.freq_dict[line_split[0]] = int(line_split[1])
    
  def __write_to_freq_dict(self):
    path = f"data_retriever_storage/news/sentiment_data/{self.__ticker}_sentiment_data.txt"
    f = open(path, 'w')
    f.write(str(self.num_articles) + "\n")
    for key in self.freq_dict.keys():
      line = key + " " + str(self.freq_dict[key]) + "\n"
      f.write(line)
  
  def __update_freq_dict(self, freq_dist):
    for key in freq_dist:
      freq = freq_dist.get(key)
      if key in self.freq_dict.keys():
        self.freq_dict[key] += int(freq) - 1
      else:
        self.freq_dict[key] = 1

  def put_all_tg(self):
    # number of articles for a stock, file names for the article data
    self.__read_in_freq_dict()
    num, article_files = self.__number_of_articles()
    self.num_articles += int(num)
    for file_name in article_files:
      file_path = f"data_retriever_storage/news/news_article_contents/{self.__ticker}/{file_name}"
      # tokenizes
      tokens_list = self.__tokenize(file_path)
      #removes noise 
      cleaned_tokens_list, mentions = self.__remove_noise(tokens_list)
      # gets all words in the generator object
      all_words = self.get_all_words(cleaned_tokens_list)
      # maps word to freq
      freq_dist = FreqDist(all_words)
      self.__update_freq_dict(freq_dist)  
      #print(cleaned_tokens_list)
    self.__write_to_freq_dict()

SA = SentimentAnalyzer('TSLA')
SA.put_all_tg()
