

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


  def tokenize(self, path):
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

  def remove_noise(self, words, ticker):
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
      if word not in words_to_ditch:
        newWords.append(word)
    return (newWords, mentions)




SA = SentimentAnalyzer()
data = SA.tokenize('data_retriever_storage/news/news_article_contents/AAPL/AAPL1.txt')
newWords, mentions = SA.remove_noise(data, 'AAPL')

print(newWords)
#path = 'data_retriever_storage/news/news_article_contents/AAPL/AAPL4.txt'


# file2 = open('wordlists2.txt', 'w')
# SA = SentimentAnalyzer()
# for i in range(1, 20):
#   file2.write("File " + str(i) + "\n")
#   path = f'data_retriever_storage/news/news_article_contents/TSLA/TSLA{i}.txt'
#   ticker = path[path.rindex('/') + 1 : path.rindex("A") + 1]
#   words = SA.tokenize(path)
#   newWords, mentions = SA.remove_noise(words, ticker)
#   freq = word_freq(newWords)
#   FREQUENT = []
#   sorted_values = sorted(freq.values())
#   for key in freq.keys():
#     if freq[key] > 9:
#       file2.write(key + ': ' + str(freq[key]) + ' occurences')
#       file2.write('\n')
# file2.close()

# path = 'wordlists2.txt'
# file3 = open(path, 'r')
# freqs = {}
# for line in file3:
#   list1 = line.split()
#   if list1[0] == "File":
#     continue
#   if list1[0] in freqs.keys():
#     freqs[list1[0]] += 1
#   else:
#     freqs[list1[0]] = 1
# words_to_ditch = []
# for key, value in freqs.items():
#   if value > 5:
#     words_to_ditch.append(key)

# print(words_to_ditch)