from account_data_retriever import AccountDataRetriever
import models.webpage as webpage

ADR = AccountDataRetriever()

html_top_content = webpage.DOCTYPE + webpage.HEAD + '''
  
  <div class="nav-bar">
    <a href="/">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="/static/logo.mp4" type="video/mp4">
      </video>
    </a>
    <ul class="nav-buttons">
      <li class="button color"><a style = "text-decoration: none; color: white" href="#top">Portfolio</a></li>
      <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
      <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
    </ul>
  </div>
  <div class="scroll custom-scrollbar">
    <table class="holdings-table" style="background-color:#050505; border-collapse:collapse;">
      <tr style="text-align:center">
        <th>Stock</th>
        <th>Daily % Change</th>
        <th>Avg Cost</th>
        <th>Current Price</th>
        <th>Shares Owned</th>
        <th>Market Value</th>
        <th>Total P/L</th>
      </tr>
      {% for holding in holdings %}
          <tr target="_blank" onclick="window.open('https://www.marketwatch.com/investing/stock/{{holding[0]}}', '_blank')" style="text-align:center; background-color: {{holding[9]}}; cursor: pointer" class="zoom">
            <td>{{holding[0]}}</td>
            <td style="color:{{holding[7]}}">{{holding[1]}}</td>
            <td>{{holding[2]}}</td>
            <td>{{holding[3]}}</td>
            <td>{{holding[4]}}</td>
            <td>{{holding[5]}}</td>
            <td style="color:{{holding[8]}}">{{holding[6]}}</td>
          </tr>
      {% endfor %}
  </div>
'''




