class NewsArticle:
  '''
  NEWS ARTICLE MODEL
  '''
  
  def __init__(self, title="", url="", contents="") -> None:
      self.title = title
      self.url = url
      self.contents = contents

  def listify(self) -> list:
    ''' Returns list of class contents '''
    return [self.title, self.url, self.contents]

  