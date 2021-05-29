

class SentimentAnalyzer:
  '''
  Class should support
    tokenizing
    removing noise
    determining density
    the actual model
    testing the model
  
  
  '''
  def __init__(self) -> None:
    self.__tickers = {
      'AAPL' : ['aapl', 'apple', 'tim', 'cook', 'iphone'], 
      'AMZN' : ['amzn', 'amazon', 'jeff', 'bezos'], 
      'TSLA' : ['tsla', 'elon', 'tesla', 'roadster', 'musk', 'meme', 'doge']
    }

  def update_tickers(self, ticker, common_phrases):
    '''
    REQUIRES: str (ALL CAPS) representing ticker, list of strings (all lowercase) 
              representing phrases
    EFFECTS:  updates tickers dictionary
    '''
    self.__tickers[ticker] = common_phrases


  def retrieve_words(self, path):
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

  def tokenize(self, words, ticker):
    '''
    REQUIRES: list representing unrefined words from article, string (ALL CAPS) 
              representing ticker
    MODIFIES: tokenizes the data. removes punctuation, makes all words lowercase,
              maintains percentages, removes numbers if not part of a percentage
    EFFECTS:  returns tuple containing tokenized words and the number of mentions
              of the desired ticker
    '''
    punctuation = '''#@,();:?/-|—.\^$'''
    mentions = 0
    newWords = []
    for word in words:
      word = word.lower()
      if '%' not in word:
        if "’s" in word:
          word = word.replace("’s", "")
        elif "'s" in word:
          word = word.replace("'s", "")
        for ch in word:
          if ch in punctuation:
            word = word.replace(ch, "")
        if word.isdigit():
          continue
      if word in self.__tickers[ticker]:
        mentions += 1
      newWords.append(word)
    return (newWords, mentions)


path = 'data_retriever_storage/news/news_article_contents/AAPL/AAPL4.txt'
ticker = path[path.rindex('/') + 1 : path.rindex(".") - 1]

SA = SentimentAnalyzer()
words = SA.retrieve_words(path)
newWords, mentions = SA.tokenize(words, ticker)
print(newWords)
