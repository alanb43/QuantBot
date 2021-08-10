  
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
      <li class="button color"><a style = "text-decoration: none; color: inherit" href="/contact">Contact Us</a></li>
    </ul>
  </div>
  <div class="header" style="text-align: center; width: 60%; margin: 0 auto">
    <p class="header-p" style="font-size: 50px; margin-bottom: 0; margin-top: 100px; color: white" >{{header[0]}}</p>
    <p class="header-p" style="font-size: 12px; color: yellow;">Total Portfolio Value</p>
    <p style="font-size: 13px; text-align: left; color: white; margin-bottom: 35px">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus vel tincidunt nibh, a lobortis enim. Curabitur eu dui velit. Donec imperdiet augue in aliquam scelerisque. Suspendisse fermentum neque dui, eget blandit nibh aliquet vitae. Sed non augue id lorem viverra gravida. Nullam pharetra magna sed augue commodo, a iaculis enim porta. Quisque feugiat magna quis arcu interdum pulvinar at at purus. Cras ipsum dui, sodales sit amet convallis nec, venenatis id est. Sed pharetra justo magna, sed pharetra felis vehicula ut. Proin ut orci mi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent rutrum mauris et risus mattis pulvinar. Nulla at ante sapien. Ut euismod vitae dui gravida malesuada.</p>
  </div>
  <div class="scroll custom-scrollbar" style="margin-top: 0">
    <table class="holdings-table" style="background-color:#050505; border-collapse:collapse;">
      <tr style="text-align:center; border-bottom: 1px solid gray">
        <th>Stock</th>
        <th>Daily % Change</th>
        <th>Avg Cost</th>
        <th>Current Price</th>
        <th>Shares Owned</th>
        <th>Market Value</th>
        <th>Total P/L</th>
      </tr>
      {% for holding in holdings %}
          <tr class="row" target="_blank" onclick="window.open('https://www.marketwatch.com/investing/stock/{{holding[0]}}', '_blank')" style="text-align:center; background-color: {{holding[9]}}; cursor: pointer; z-index: 1">
            <td>{{holding[0]}}</td>
            <td style="color:{{holding[7]}}">{{holding[1]}}</td>
            <td>{{holding[2]}}</td>
            <td>{{holding[3]}}</td>
            <td>{{holding[4]}}</td>
            <td>{{holding[5]}}</td>
            <td style="color:{{holding[8]}}">{{holding[6]}}</td>
          </tr>
      {% endfor %}
    </table>
  </div>
  <ul style="list-style: none; display: flex; flex-direction: horizontal; width: 100%; margin-left: 25%; margin-top: 125px; margin-bottom: 50px">
    <li style="margin-right: 25%"><div id="chartContainer"></div></li>
    <li><div id="chartContainer2"></div></li>
  </ul>
  <div style="height: 500px"></div>
  
</body>
'''







