
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
from bs4 import BeautifulSoup

channel_layer = get_channel_layer()

@shared_task()
def get_live_price(arg1 , arg2):
    url = 'https://finance.yahoo.com/quote/'+arg1+'.NS'
    page = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    soup = BeautifulSoup(page.text, 'html.parser')
    price = soup.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    diff = soup.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    percent = soup.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].find('span').text
    
    context = {
        'price': price,
        'diff': diff,
        'percent': percent,
    }
    
    async_to_sync(channel_layer.group_send)(
        'stock_stock', {'type': 'send_data', 'context': context})
    # async_to_sync(channel_layer.group_send)(
    #     arg2, {'type': 'send_data', 'context': arg1})
    
# def update_task_schedule(arg1, arg2):
#     # Remove the existing schedule (if any)
#     app.conf.beat_schedule.pop('get_stock_price', None)

#     # Add the updated schedule
#     app.conf.beat_schedule['get_stock_price'] = {
#         'task': 'stock.tasks.task1',
#         'schedule': 3.0,  # Run every 3 seconds
#         'args': (arg1, arg2),  # Pass your updated arguments here
#     }

    
#     # task1.apply_async(args=[json_params], countdown=3)
# def stop_task():
#     global is_connected
#     is_connected = False

@shared_task
def get_index_data(arg1):
    # SENSEX DATA
    url1 = 'https://finance.yahoo.com/quote/%5EBSESN?p=%5EBSESN'
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
    url2 = 'https://finance.yahoo.com/quote/%5ENSEI?p=%5ENSEI&.tsrc=fin-srch'
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
    url3 = 'https://finance.yahoo.com/quote/%5ENSEBANK?p=%5ENSEBANK&.tsrc=fin-srch'
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

    # NIFTY-IT DATA
    url4 = 'https://finance.yahoo.com/quote/%5ECNXIT/'
    page4 = requests.get(url4, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    soup4 = BeautifulSoup(page4.text, 'html.parser')
    price4 = soup4.find(
        'fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    diff4 = soup4.find(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    percent4 = soup4.find_all(
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
        'price4': price4,
        'diff4': diff4,
        'percent4': percent4,
    }

    async_to_sync(channel_layer.group_send)('index_data', {'type':'send_data', 'context':context})
    # async_to_sync(channel_layer.group_send)(
    #     'index_data', {'type': 'send_data', 'context': context})


@shared_task
def get_top_gainers(arg1):

    url = 'https://groww.in/v1/api/stocks_data/explore/v2/indices/GIDXNIFTY100/market_trends?discovery_filter_types=TOP_GAINERS&size=4'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,mr;q=0.7,hi;q=0.6",
        "authorization": "",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-app-id": "growwWeb",
        "x-device-id": "8124d544-dbe8-508b-a340-4117e503a4af",
        "x-device-type": "msite",
        "x-platform": "web",
        "x-request-checksum": "N2FwcjlyIyMjVjNkVmVvalB5U0RCSUNJa2dSMHVCczVVOGhRdlIrWC9TbXUvb2oyMUlyYkY3RmVlbU5SUXcxUktWdHlLdm5XenVVYmRMTXJUeUdxWkdyekkyYU5nSXVrN0J1ZGoxQm40RkdyWkE4bDR5K1k9",
        "x-request-id": "6d779dbf-d104-433e-9bef-e137c610847c",
        "x-user-campaign": "",
        "cookie": "bfdskfds=light; _gcl_au=1.1.1182045085.1685456864; _gid=GA1.2.1594145463.1685456864; g_state={\"i_p\":1685464431727,\"i_l\":1}; we_luid=d215c74fe79a09830b3867d79bc7c61251daf352; __cf_bm=VgyKalPwMB1zWiFvH6PI6cHp_Sofx7ucskXw3xM0LPU-1685462941-0-AWJ6H7CbGJ/vsoQ5NruQGd8F8OXNaUtb5QGCauenjjp7PgCTGv7Z320SQbv8HtgvS+JHqqkI5+ch3gyH+2vTEqQ=; __cfruid=41f497d3ac0fcaa41a5840ab09d5544dd9878ab5-1685462941; _cfuvid=WyX.qZo77RjoVcZoz39A9rwejGNBP8N9ImLX1MMiDr4-1685462941819-0-604800000; _ga=GA1.1.1610518639.1685456864",
        "Referer": "https://groww.in/markets/top-gainers",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url, headers=headers)
    context = {}
    if response.status_code == 200:
        data = response.json()
        context['data'] = []
        context['price'] = []
        context['diff'] = []
        for i in range(4):
            context['data'].append(
                data['categoryResponseMap']['TOP_GAINERS']['items'][i]['company']['companyName'])
            context['price'].append(
                data['categoryResponseMap']['TOP_GAINERS']['items'][i]['stats']['ltp'])
            context['diff'].append(str("{:.2f}".format(data['categoryResponseMap']['TOP_GAINERS']['items'][i]['stats']['dayChange'])) +
                                   " ("+str("{:.2f}".format(data['categoryResponseMap']['TOP_GAINERS']['items'][i]['stats']['dayChangePerc']))+"%)")
    else:
        print("Request failed with status code:", response.status_code)
    
    async_to_sync(channel_layer.group_send)('top_gainers_data', {'type':'send_tg_data','context':context})
    # async_to_sync(channel_layer.group_send)(
        # 'top_gainers_data', {'type': 'send_tg_data', 'context': context})


@shared_task
def get_top_losers(arg1):

    url = 'https://groww.in/v1/api/stocks_data/explore/v2/indices/GIDXNIFTY100/market_trends?discovery_filter_types=TOP_LOSERS&size=4'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,mr;q=0.7,hi;q=0.6",
        "authorization": "",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-app-id": "growwWeb",
        "x-device-id": "8124d544-dbe8-508b-a340-4117e503a4af",
        "x-device-type": "msite",
        "x-platform": "web",
        "x-request-checksum": "N2FwcjlyIyMjVjNkVmVvalB5U0RCSUNJa2dSMHVCczVVOGhRdlIrWC9TbXUvb2oyMUlyYkY3RmVlbU5SUXcxUktWdHlLdm5XenVVYmRMTXJUeUdxWkdyekkyYU5nSXVrN0J1ZGoxQm40RkdyWkE4bDR5K1k9",
        "x-request-id": "6d779dbf-d104-433e-9bef-e137c610847c",
        "x-user-campaign": "",
        "cookie": "bfdskfds=light; _gcl_au=1.1.1182045085.1685456864; _gid=GA1.2.1594145463.1685456864; g_state={\"i_p\":1685464431727,\"i_l\":1}; we_luid=d215c74fe79a09830b3867d79bc7c61251daf352; __cf_bm=VgyKalPwMB1zWiFvH6PI6cHp_Sofx7ucskXw3xM0LPU-1685462941-0-AWJ6H7CbGJ/vsoQ5NruQGd8F8OXNaUtb5QGCauenjjp7PgCTGv7Z320SQbv8HtgvS+JHqqkI5+ch3gyH+2vTEqQ=; __cfruid=41f497d3ac0fcaa41a5840ab09d5544dd9878ab5-1685462941; _cfuvid=WyX.qZo77RjoVcZoz39A9rwejGNBP8N9ImLX1MMiDr4-1685462941819-0-604800000; _ga=GA1.1.1610518639.1685456864",
        "Referer": "https://groww.in/markets/top-gainers",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url, headers=headers)
    context = {}
    if response.status_code == 200:
        data = response.json()
        context['data'] = []
        context['price'] = []
        context['diff'] = []
        for i in range(4):
            context['data'].append(
                data['categoryResponseMap']['TOP_LOSERS']['items'][i]['company']['companyName'])
            context['price'].append(
                data['categoryResponseMap']['TOP_LOSERS']['items'][i]['stats']['ltp'])
            context['diff'].append(str("{:.2f}".format(data['categoryResponseMap']['TOP_LOSERS']['items'][i]['stats']['dayChange'])) +
                                   " ("+str("{:.2f}".format(data['categoryResponseMap']['TOP_LOSERS']['items'][i]['stats']['dayChangePerc']))+"%)")
    else:
        print("Request failed with status code:", response.status_code)

    async_to_sync(channel_layer.group_send)('top_losers_data',{'type':'send_tl_data','context':context})
    # async_to_sync(channel_layer.group_send)(
    #     'top_losers_data', {'type': 'send_tl_data', 'context': context})