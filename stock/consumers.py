from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
import json
from urllib.parse import parse_qs
# from .tasks import update_task_schedule


class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'index'
        self.room_group_name = 'index_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def send_data(self, event):
        price = event['context']
        await self.send(json.dumps(price))

class TopGainersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'top_gainers'
        self.room_group_name = 'top_gainers_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def send_tg_data(self, event):
        tg_data = event['context']
        await self.send(json.dumps(tg_data))


class TopLosersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'top_losers'
        self.room_group_name = 'top_losers_data'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def send_tl_data(self, event):
        tl_data = event['context']
        await self.send(json.dumps(tl_data))

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from asgiref.sync import sync_to_async, async_to_sync
class StockPriceConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, arg1):
        task = PeriodicTask.objects.filter(name='get_stock_price')
        if task:
            # Update existing task
            task = task.first()
            args = json.loads(task.args)
            print(args)
            args = args[0]
            print(args)
            print(arg1)
            for x in arg1:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            # Create new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='get_stock_price',
                task='stock.tasks.task1',  # Update the path to your dynamic_task function
                args=json.dumps([arg1])
            )


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sym']
        self.room_group_name = 'stock_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        query_params = parse_qs(self.scope["query_string"].decode())
        # print(query_params)

        symbol = query_params['symbol']
        # print(symbol)

        params = {
            'symbol':symbol,
            'name': self.room_group_name
        }
        # print([symbol])
        await self.addToCeleryBeat(symbol)
        # task1.delay(symbol, self.room_group_name)
        # await self.update_task_schedule(symbol[0], self.room_group_name)
        
        # json_params = json.dumps(params)

        # task1.apply_async(args=[json_params], countdown=3)

        await self.accept()

    # async def update_task_schedule(self, arg1, arg2):
    #     # Remove the existing schedule (if any)
    #     print("hello")
    #     app.conf.beat_schedule.pop('get_stock_price', None)
    #     print("hello")
    #     # Add the updated schedule
    #     current_app.conf.beat_schedule['get_stock_price'] = {
    #         'task': 'stock.tasks.task1',
    #         'schedule': 3.0,  # Run every 3 seconds
    #         'args': (arg1, arg2,),  # Pass your updated arguments here
    #     }
    #     print(app.conf.beat_schedule)


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def send_data(self, event):
        data = event['context']
        # print(data)
        await self.send(json.dumps(data))
    