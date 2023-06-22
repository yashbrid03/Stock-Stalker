# Stock-Stalker
This application visualize the stock performance and stats and also predict stock values in future

## Snippets (Till now)
![image](https://github.com/yashbrid03/Stock-Stalker/assets/65955929/052e423b-7029-4756-8809-74e3d46b644e)

![image](https://github.com/yashbrid03/Stock-Stalker/assets/65955929/ef2c69a2-ccc3-46a4-941a-ab634ac5b631)

![image](https://github.com/yashbrid03/Stock-Stalker/assets/65955929/0e444c0e-34b2-4125-9d12-d253b20b649d)


## Architecture
![A4 - 1](https://github.com/yashbrid03/Stock-Stalker/assets/65955929/2fbde452-4fd2-4d07-8c54-9af792478ede)

- First user sends HTTP request to Django and it responds with HTTP response
- Now client establishes websocket connection for specific task to be done. Each websocket is related to a consumer.
- After that celery beat schedule the task and send its to broker (we are using redis as broker)
- Now celery worker takes the task from broker and perform actual task and send results to Django (Actually it sends results to consumer and consumer send to client through ws)
- Django responds with Ajax request which includes data

## How to start
- start the redis server
- start the Django project by running following command in cmd  `python manage.py runserver`
- Start the celery Beat scheduler by running following command in another cmd `celery -A realtime beat -l INFO`
- Start the celery Worker by running following command in another cmd `celery -A realtime worker -l INFO -P eventlet`

## Progress
- Done with the Homepage
  - On homepage you can see realtime index such as Nifty50, Sensex, NiftyBank and NiftyIt.
  - Also you can see realtime Top Gainers and Top Losers of the current day.
  - Search functionality to search individual stocks
- Individual Page
  - On individual page you can see the basic info of the stocks (like market cap, volume, P.E. ratio etc)
  - Along with that you can see the Stock Analysis (for eg its Trend, EMA, SMA, MA, etc.)

## Remaining Tasks
- Creating seperate page for Top losers and top gainers
- Analysis Part is remaining (40%)
- Realtime Price on individual stock page (celery task is created, only web scraping logic is remaining)
- Implementation of ML model to predict stock price

## Limitations
- It is not feasible to make one ML model for every stock. because every stock has its own different behaviour/timeseries.
- because model trained on one stocks timeseries cannot predict other stock price

## Alternative
- Make ML model that is trained on multiple dataset of stock price. (still it is not proper way.)
- Build ML model in runtime for the searched stock (Time consuming and if one stock is searched multiple times it will build again and again for same stock)
- Build ML model for searched stock and store it in database, when next time the same stock is searched, perform lookup in DB. (still not feasible because stock data changes over a period)



