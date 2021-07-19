from dataclasses import dataclass

@dataclass
class Article:
  ''' NEWS ARTICLE MODEL '''
  
  title: str
  url: str
  date: str
  contents: str

  def listify(self) -> list:
    ''' Returns list of class contents '''
    return [self.title, self.url, self.date, self.contents]

  