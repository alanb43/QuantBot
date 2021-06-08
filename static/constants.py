TOP_OF_PAGE = '''
  <!DOCTYPE html>
  <head>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://use.typekit.net/oxi4xqh.css">
    <title>QuantBot</title>
    <link rel="shortcut icon" href="resources/favicon.ico">
  </head>
  <body>
    <div class="nav-bar">
      <a href="QuantBot.io">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="resources/logo.mp4" type="video/mp4">
      </video>
    </a>
      <ul class="nav-buttons">
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#top">Portfolio</a></li>
        <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
      </ul>
    </div>
    <div class="side-bar">
      <p class="holdings">Current Holdings</p>
      <ul class="shares">
'''

MIDDLE_PAGE = '''
</ul>
  </div>
  <div class="body">
    <h1 id="top" class="num">${self.get_equity()[1]}</h1>
    <h2 class="color num">{self.get_account_daily_change()[1]} ({self.get_account_percent_change()[1]}%)</h2>
    {graph_div}
    <div class="buyingpower">
        <p class="buy">Buying Power</p>
        <p class="buy2 num">${self.get_buying_power()[1]}</p>
    </div>
    <div class="summary">
      <p class="color" style="font-weight: bold">What is Quantbot?</p>
      <p class="des">Quantbot is a Python Bot that utilizes a combination of machine learning, time analysis, and sentiment analysis to automatically buy and sell stocks. The bot uses a web scraper that periodically checks for new articles regarding a company and analyzes the content in the article. If the bot deems the article particularly positive or negative for that company, the bot will either buy or sell the shares we have.</p>
    </div>
    <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
    <div class="news">
'''

BOTTOM_OF_PAGE = '''
    <div class="contact color" id="contact">
          <h3 style="margin-bottom: -10px; font-size: 18px;">Contact Us</h3>
          <p style="margin-bottom: -10px; font-size: 15px;">Josh Cunningham || jcun@umich.edu || LinkedIn</p>
          <p style="font-size: 15px">Alan Bergsneider || bera@umich.edu || LinkedIn</p>
    </div>
  </div>
</body>
'''