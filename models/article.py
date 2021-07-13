class Article:
  '''
  NEWS ARTICLE MODEL
  '''
  
  def __init__(self, title="", url="", date="", contents="") -> None:
      self.title = title
      self.url = url
      self.date = date
      self.contents = contents

  def listify(self) -> list:
    ''' Returns list of class contents '''
    return [self.title, self.url, self.date, self.contents]

  