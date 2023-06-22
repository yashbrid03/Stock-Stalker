from django.urls import path
from .consumers import  IndexConsumer, TopGainersConsumer, TopLosersConsumer, StockPriceConsumer

ws_urlpatterns = [
    path('ws/index/', IndexConsumer.as_asgi()),
    path('ws/top_gainers/', TopGainersConsumer.as_asgi()),
    path('ws/top_losers/', TopLosersConsumer.as_asgi()),
    path('ws/stockprice/<str:sym>', StockPriceConsumer.as_asgi()),
]