# Get live prices of stock from Yahoo Finance
from bs4 import BeautifulSoup
import requests

while True:
    # get the URL of the page
    url = 'https://finance.yahoo.com/quote/TCS.NS?p=TCS.NS&.tsrc=fin-srch'

    # request the page with url and headers
    page = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })

    # using BeautifulSoup extract the data
    soup = BeautifulSoup(page.text, 'html.parser')

    # current price
    price = soup.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text

    # difference between current price and previous close price
    diff = soup.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text

    # percentage difference between current price and previous close price
    percent = soup.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].text

    print(price+" "+diff+" "+percent)
