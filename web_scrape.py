import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# URL we want to scrape data from
url = 

# We connect to the URL (response code 200 desired)
response = requests.get(url)

# We parse the HTML and save it to a BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

