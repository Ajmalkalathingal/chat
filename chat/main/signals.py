from django.db.models.signals import post_save
from django.dispatch import receiver
from chatapp.models import UserProfile
from .models import Notificaton
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=UserProfile)
def send_onlinestatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.user.username
        user_id = str(instance.id)
        user_status = instance.online_status
        # print('status',user_status)

        data = {
            'username':user,
            'status':user_status
        }

        async_to_sync(channel_layer.group_send)(
            'user',
            {
                'type': 'send_onlineStatus',
                'value': json.dumps(data)
            }
        )# two argument group name and data here 'user' is group name (group name set in consumer.py online consumer)

        
# @receiver(post_save, sender=Notificaton)
# def Get_notification(sender, instance, created, **kwargs):
#     # print("Get_notification triggered")

#     if created:
#         channel_layer = get_channel_layer()
#         print(instance)
#         user = instance.user
#         notification_obj = Notificaton.objects.filter(is_seen=False, user=user.id,).count()
#         # print(notification_obj)
#         room_name = str(instance.user.id)

#         data = {
#             'count': notification_obj
#         }

#         # print(f'signal group name {room_name}')

#         async_to_sync(channel_layer.group_send)(
#             room_name, {
#                 'type': 'send_notifications',
#                 'value': json.dumps(data)
#             }
#         )




@receiver(post_save, sender=Notificaton)
def get_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user = instance.user
        notification_obj = Notificaton.objects.filter(is_seen=False, user=user.id).count()
        room_name = str(user.id)

        data = {
            'count': notification_obj
        }

        async_to_sync(channel_layer.group_send)(
            room_name, {
                'type': 'send_notifications',
                'value': json.dumps(data)
            }
        )    