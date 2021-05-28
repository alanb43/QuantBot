from nltk.corpus import twitter_samples

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
more_tokens = twitter_samples.tokenized('negative_tweets.json')

path = 'data_retriever_storage/news/news_article_contents/AAPL/AAPL17.txt'

file = open(path, 'r')

outfile = open('output.txt', 'w')

for line in file:
  outfile.write(line)

class SentimentAnalyzer:
  def __init__(self) -> None:
      pass

