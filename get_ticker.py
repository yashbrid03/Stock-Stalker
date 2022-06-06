from fileinput import filename
import requests
from bs4 import BeautifulSoup
import csv

# url from where list of ticker symbol is scraped
url = "https://indiancompanies.in/listed-companies-in-nse-with-symbol/"
r = requests.get(url)
count = 0
quotes = [""]
quote = {}
soup = BeautifulSoup(r.content, "html.parser")

for row in soup.find_all('td'):
    if count == 1:
        quote['cmp'] = row.text
        count = count + 1
    elif count == 2:
        quote['ticker'] = row.text+".NS"
        count = count - 2
        # print(quote)
        quotes.append(quote)
    else:
        count = count + 1
        quote = {}

# print(quotes)

del quotes[0]  # deleting 1st element which is ""
# deleting 1st element which is {'cmp': 'NAME OF COMPANY', 'ticker': 'SYMBOL.NS'}
del quotes[0]
keys = quotes[0].keys()
fileName = 'ticker.csv'

with open(fileName, 'w', newline='') as f:
    w = csv.DictWriter(f, keys)
    w.writeheader()
    for dictionary in quotes:
        w.writerow(dictionary)
