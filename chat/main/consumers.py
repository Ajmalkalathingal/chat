from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async 
from .models import Chat,Notificaton  
from chatapp.models import User,UserProfile

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print('websocket connected')
        self.my_id = self.scope['user'].id
        self.other_user_id = self.scope['url_route']['kwargs']['id']

        if int(self.my_id) > int(self.other_user_id):
            self.room_name = f'{self.my_id}-{self.other_user_id}'
        else:
            self.room_name = f'{self.other_user_id}-{self.my_id}'

        self.group_room_name = f'chat_{self.room_name}' 

        await self.channel_layer.group_add(self.group_room_name,self.channel_name)

        await self.accept() 
        await self.send(self.group_room_name)


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        user_name = data['username']
        receiver = data['receiver']
        
        # save message
        await self.chatMessageSave(user_name,self.group_room_name,message,receiver) 

        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'chat.message',
                'message': message,
                'username':user_name,
                'receiver':receiver
            }
        )

    async def chat_message(self, event):        
        await self.send(json.dumps({
            'message':event['message'],
            'username':event['username'],
            'receiver':event['receiver'],
        }))    

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_room_name, self.channel_name
        )
    
    @database_sync_to_async
    def chatMessageSave(self,username,thread_name,message,receiver):
        user = User.objects.get(username=username)
        message = Chat.objects.create(sender=user,message=message,theard_name=thread_name)
        other_user_id = self.scope['url_route']['kwargs']['id']
        get_user = User.objects.get(id=other_user_id)

        try:
            receiver_user = User.objects.get(email=receiver)
        except User.DoesNotExist:
            print("Receiver user not found")
            return

        if receiver_user.id == get_user.id:
            try:
                notification = Notificaton.objects.create(message=message, user=receiver_user)
            except Exception as e:
                print(f"Error creating notification: {e}")
        # print(notification)        

    #  =============================================================================#
                

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['user'].id
#         self.room_group_name = f'{self.user_id}'
#         print(f'WebSocket CONNECTz {self.room_group_name}')
        
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()



#     async def disconnect(self, event):
#          await self.channel_layer.group_discard(
#              self.room_group_name,
#              self.channel_name
#          )
                             
#     async def send_notifications(self, event):

#         # print("send_notification triggered")
#         data = json.loads(event.get('value'))
#         # print(data)
#         notification_message_count = data['count']
#         # print(notification_message_count)

#         await self.send(json.dumps({
#             "count": notification_message_count,
#         }))
        
                    


class OnlineSatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # print('connected')
        self.group_room_name = 'user'

        await self.channel_layer.group_add(
            self.group_room_name,
            self.channel_name
        )
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        # print('username:', username)
        # print('connection type', connection_type)

        await self.online_status_update(username,connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value')) #event from signals (value is the dictionsry) in signals.py 
        username = data['username']
        online_status = data['status']
        # print('online status', online_status)   
        # print('username', username) 

        await self.send(json.dumps(
            {
                "username":username,
                "status":online_status
            }
        ))  


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_room_name,
            self.channel_name
        )
 

    @database_sync_to_async
    def online_status_update(self, username,online_status):
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        if online_status == 'open':
            user_profile.online_status = True
            user_profile.save()

        else:
            user_profile.online_status = False
            user_profile.save()  




class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.room_group_name = f'{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Get the initial notification count and send it to the client
        initial_notification_count = await self.get_initial_notification_count()
        await self.send_notification({
            'type': 'initial_notification_count',
            'count': initial_notification_count,
        })

    async def send_notification(self, event):
        await self.send(json.dumps(event))


    async def send_notifications(self, event):
        data = json.loads(event.get('value'))
        notification_message_count = data['count']
        print(notification_message_count)
        
        await self.send(json.dumps({
            "count": notification_message_count,
        }))

    @database_sync_to_async
    def get_initial_notification_count(self):
        user = User.objects.get(id=self.user_id)
        return Notificaton.objects.filter(user=user, is_seen=False).count()
    

    async def disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
