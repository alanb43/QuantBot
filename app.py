from flask import Flask, render_template
from webpage_data_refresher import WebpageDataRefresher
app = Flask(__name__)

@app.route("/")
def main():
  WDR = WebpageDataRefresher()
  WDR.create_site_html()
  return render_template('index.html', WDR=WDR)

