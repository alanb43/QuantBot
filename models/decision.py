from dataclasses import dataclass

@dataclass
class Decision:
  symbol: str
  decision: str
  shares_moved: str
  url: str
  title: str
  intro: str

  def listify(self) -> list:
    ''' Returns list of class contents '''
    return [self.symbol, self.decision, self.shares_moved, self.url, self.title, self.intro]
  