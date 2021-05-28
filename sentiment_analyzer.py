from nltk.corpus import twitter_samples

# positive_tweets = twitter_samples.strings('positive_tweets.json')
# negative_tweets = twitter_samples.strings('negative_tweets.json')
# text = twitter_samples.strings('tweets.20150430-223406.json')
# tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
# more_tokens = twitter_samples.tokenized('negative_tweets.json')

path = 'data_retriever_storage/news/news_article_contents/AAPL/AAPL4.txt'

file = open(path, 'r')


# keep_skipping = True
# article_words = []

# for line in file:
#   if len(line.split()) > 2:
#     keep_skipping = False
#   if keep_skipping or len(line.split()) == 0:
#     continue
#   a = list(line.split())
#   article_words += a

# for word in article_words:
#   print(word)


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
    pass

