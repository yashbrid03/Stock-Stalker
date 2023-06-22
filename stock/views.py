from django.shortcuts import render
import pandas as pd
import yfinance as yf
import locale
import numpy as np
# Create your views here.

df = pd.read_csv('static/ticker.csv', encoding='latin-1')

def format_cash(amount):
    def truncate_float(number, places):
        return int(number * (10 ** places)) / 10 ** places

    if amount < 1e3:
        return amount

    if 1e3 <= amount < 1e5:
        return str(truncate_float((amount / 1e5) * 100, 2)) + " K"

    if 1e5 <= amount < 1e7:
        return str(truncate_float((amount / 1e7) * 100, 2)) + " L"

    if amount > 1e7:
        return str(truncate_float(amount / 1e7, 2)) + " Cr"
    
def index(request): 
    context = {
        "ticker": df["company"],
    }
    return render(request, 'index.html', context)

def stock(request):
    if request.method == 'POST':
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        search_value = request.POST.get('default-search')
        print(search_value)
        ticker = df.loc[df['company'] == search_value, 'ticker'].values[0]
        # print(search_value)
        sym = yf.Ticker(ticker)

        # Basic info
        info = sym.info
        short_summary = ' '.join(info['longBusinessSummary'].split()[:50])
        remain_summary = ' '.join(info['longBusinessSummary'].split()[50:])
        marketcap = format_cash(info['marketCap'])
        totalcash = format_cash(info['totalCash'])
        totaldebt = format_cash(info['totalDebt'])
        totalrevenue = format_cash(info['totalRevenue'])
        roeinperc = "{:.2f}%".format(info['returnOnEquity'] * 100)
        dyinperc = "{:.2f}%".format(info['dividendYield'] * 100)
        # print(sym.info)

        # chart
        df1 = sym.history(period="5mo")
        df1.index = df1.index.strftime('%Y-%m-%d')

        df1 = df1.reset_index()
        labels = df1['Date'].tolist()
        actualclose = df1['Close'].tolist()
        df1['SMA20'] = df1['Close'].rolling(20).mean()
        df1['SMA20'] = df1['SMA20'].fillna('NaN')
        SMA = df1['SMA20'].tolist()
        df1['CMA20'] = df1['Close'].expanding().mean()
        df1['CMA20'] = df1['CMA20'].fillna('NaN')
        CMA = df1['CMA20'].tolist()
        df1['EWMA20'] = df1['Close'].ewm(span=20).mean()
        df1['EWMA20'] = df1['EWMA20'].fillna('NaN')
        EMA = df1['EWMA20'].tolist()
        z = np.polyfit(df1.index, df1['Close'], 1)
        p = np.poly1d(z)
        trend = p(df1.index).tolist()
        colortrend = []
        if(trend[1] < trend[2]):
            colortrend = ["#089e38", "#00ff52"]
        else:
            colortrend = ["#9e1f08", "#ff2801"]

        return render(request, 'stock.html', {'search_value': ticker, 'name': info['shortName'], 'website': info['website'], 'df': sym.info, 'ticker': ticker.split('.')[0], 'summary': info['longBusinessSummary'], 'short_summary': short_summary,
                                              'remain_summary': remain_summary, 'industry': info['industry'], '52weekh': info['fiftyTwoWeekHigh'], '52weekl': info['fiftyTwoWeekLow'], 'marketcap': marketcap, 'roe': roeinperc,
                                              'bookvalue': info['bookValue'], 'dividendyield': dyinperc, 'totalCash': totalcash, 'totalDebt': totaldebt, 'totalRevenue': totalrevenue, 'quickRatio': ['quickRatio'], 'currentRatio': info['currentRatio'],
                                              'debtToEquity': info['debtToEquity'], 'returnOnAssets': info['returnOnAssets'], 'closedata': actualclose, 'trenddata': trend, 'labelstrend': labels, 'colortrend': colortrend, 'SMA': SMA, 'CMA': CMA, 'EMA': EMA})

    return render(request, 'stock.html', {'search_value': 'mello'})