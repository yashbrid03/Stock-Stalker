from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def marketoverview(request):
    from bs4 import BeautifulSoup
    import requests
    url1 = 'https://finance.yahoo.com/quote/%5EIXIC?p=%5EIXIC&.tsrc=fin-srch'
    url2 = 'https://finance.yahoo.com/quote/%5ENSEI?p=%5ENSEI&.tsrc=fin-srch'
    url3 = 'https://finance.yahoo.com/quote/%5ENSEBANK?p=%5ENSEBANK&.tsrc=fin-srch'

    # SENSEX DATA
    page1 = requests.get(url1, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    soup1 = BeautifulSoup(page1.text, 'html.parser')
    price1 = soup1.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    diff1 = soup1.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    percent1 = soup1.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].find('span').text

    # NIFTY 50 DATA
    page2 = requests.get(url2, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    soup2 = BeautifulSoup(page2.text, 'html.parser')
    price2 = soup2.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    diff2 = soup2.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    percent2 = soup2.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].find('span').text

    # NIFTY BANK DATA
    page3 = requests.get(url3, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    soup3 = BeautifulSoup(page3.text, 'html.parser')
    price3 = soup3.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    diff3 = soup3.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    percent3 = soup3.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].find('span').text

    context = {
        'price1': price1,
        'diff1': diff1,
        'percent1': percent1,
        'price2': price2,
        'diff2': diff2,
        'percent2': percent2,
        'price3': price3,
        'diff3': diff3,
        'percent3': percent3,
    }
    return render(request, 'marketoverview.html', context)
