import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','realtime.settings')

app = Celery('realtime')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.conf.beat_schedule = {
    # 'get_index_data': {
    #     'task': 'stock.tasks.get_index_data',
    #     'schedule': 3.0,
    # },
    # 'get_top_gainers': {
    #     'task': 'stock.tasks.get_top_gainers',
    #     'schedule': 3.0,
    # },
    # 'get_top_losers': {
    #     'task': 'stock.tasks.get_top_losers',
    #     'schedule': 3.0,
    # }
    # 'get_stock_price':{
    #     'task': 'stock.tasks.task1',
    #     'schedule': 3.0,
    #     'args':('MSFT',),
    # }
}

app.autodiscover_tasks()