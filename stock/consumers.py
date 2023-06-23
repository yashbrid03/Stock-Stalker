from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
import json
from urllib.parse import parse_qs
# from .tasks import update_task_schedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from asgiref.sync import sync_to_async

class IndexConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self):
        task = PeriodicTask.objects.filter(name='get_index_data')
        if task:
            task = task.first()
            arg = json.loads(task.args)
            print(arg)
            count = int(arg[0])
            count += 1
            task.args = json.dumps([str(count)])
            task.save()
        else:
            # Create new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='get_index_data',
                task='stock.tasks.get_index_data',  # Update the path to your dynamic_task function
                args=json.dumps(["1"])
            )

    async def connect(self):
        # self.room_name = 'index'
        self.room_group_name = 'index_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.addToCeleryBeat()
        await self.accept()

    @sync_to_async
    def decrement_task_count(self):
        task = PeriodicTask.objects.get(name='get_index_data')
        if task:
            arg = json.loads(task.args)
            count = int(arg[0])
            count -= 1
            if count <= 0:
                task.delete()
            else:
                task.args = json.dumps([str(count)])
                task.save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.decrement_task_count()
        await self.close()

    async def send_data(self, event):
        price = event['context']
        await self.send(json.dumps(price))

class TopGainersConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self):
        task = PeriodicTask.objects.filter(name='get_top_gainers')
        if task:
            task = task.first()
            arg = json.loads(task.args)
            print(arg)
            count = int(arg[0])
            count += 1
            task.args = json.dumps([str(count)])
            task.save()
        else:
            # Create new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='get_top_gainers',
                task='stock.tasks.get_top_gainers',  # Update the path to your dynamic_task function
                args=json.dumps(["1"])
            )
    async def connect(self):
        # self.room_name = 'top_gainers'
        self.room_group_name = 'top_gainers_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.addToCeleryBeat()
        await self.accept()

    @sync_to_async
    def decrement_task_count(self):
        task = PeriodicTask.objects.get(name='get_top_gainers')
        if task:
            arg = json.loads(task.args)
            count = int(arg[0])
            count -= 1
            if count <= 0:
                task.delete()
            else:
                task.args = json.dumps([str(count)])
                task.save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.decrement_task_count()
        await self.close()

    async def send_tg_data(self, event):
        tg_data = event['context']
        await self.send(json.dumps(tg_data))


class TopLosersConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self):
        task = PeriodicTask.objects.filter(name='get_top_losers')
        if task:
            task = task.first()
            arg = json.loads(task.args)
            print(arg)
            count = int(arg[0])
            count += 1
            task.args = json.dumps([str(count)])
            task.save()
        else:
            # Create new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='get_top_losers',
                task='stock.tasks.get_top_losers',  # Update the path to your dynamic_task function
                args=json.dumps(["1"])
            )
    async def connect(self):
        # self.room_name = 'top_losers'
        self.room_group_name = 'top_losers_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.addToCeleryBeat()
        await self.accept()

    @sync_to_async
    def decrement_task_count(self):
        task = PeriodicTask.objects.get(name='get_top_losers')
        if task:
            arg = json.loads(task.args)
            count = int(arg[0])
            count -= 1
            if count <= 0:
                task.delete()
            else:
                task.args = json.dumps([str(count)])
                task.save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.decrement_task_count()
        await self.close()

    async def send_tl_data(self, event):
        tl_data = event['context']
        await self.send(json.dumps(tl_data))


class StockPriceConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, arg1):
        name = 'get_stock_price_'+arg1[0]
        print("name to add "+name)
        task = PeriodicTask.objects.filter(name='get_stock_price_'+arg1[0])
        if task:
            task = task.first()
            arg = json.loads(task.args)
            print(arg)
            count = int(arg[1])
            count += 1
            task.args = json.dumps([arg1[0],str(count)])
            task.save()
        else:
            # Create new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='get_stock_price_'+arg1[0],
                task='stock.tasks.get_live_price',  # Update the path to your dynamic_task function
                args=json.dumps([arg1[0],"1"])
            )


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sym']
        self.room_group_name = 'stock_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        query_params = parse_qs(self.scope["query_string"].decode())
        symbol = query_params['symbol']
        self.symbol = symbol[0]
        await self.addToCeleryBeat(symbol)
        await self.accept()

    @sync_to_async
    def decrement_task_count(self):
        task = PeriodicTask.objects.get(name='get_stock_price_' + self.symbol)
        if task:
            
            arg = json.loads(task.args)
            count = int(arg[1])
            count -= 1
            if count <= 0:
                task.delete()
            else:
                task.args = json.dumps([arg[0],str(count)])
                task.save()

    async def disconnect(self, close_code):
        await self.decrement_task_count()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
                 
    async def send_data(self, event):
        data = event['context']
        await self.send(json.dumps(data))
    