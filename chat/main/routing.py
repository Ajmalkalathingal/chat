from django.urls import path
from main import consumers

websocket_url = [
     path('ws/<int:id>/', consumers.MyAsyncWebsocketConsumer.as_asgi()),
     path('ws/online/', consumers.OnlineSatusConsumer.as_asgi()),
     path('ws/notification/', consumers.NotificationConsumer.as_asgi()),
]