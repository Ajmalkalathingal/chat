from django.shortcuts import render
from chatapp.models import User,UserProfile
from django.contrib.auth.decorators import login_required
from .models import Chat,Notificaton
from django.http import JsonResponse

@login_required
def index(request):
    users = User.objects.exclude(username=request.user)
    return render(request, 'app/index.html', context={'users': users})

    
@login_required    
def main_chat(request, username):
    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(id=request.user.id)
    
    
    for user in users:
        user.notification_count = Notificaton.objects.filter(user=user, is_seen=False).count()

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'

    messages = Chat.objects.filter(theard_name=thread_name)

    context = {
        'users': users,
        'user': user_obj,
        'messages': messages,
        # 'notification_count': notification_count
    }

    return render(request, 'app/main_chat.html', context)




# checking
    # for user in users:
    #     print(f"{user.username} - Online Status: {user.userprofile.online_status}")
    
    # Get the notification count for each user
    # notification_count = {}
    # for user in all_users:
    #     count = Notificaton.objects.filter(user=user, is_seen=False).count()
    #     notification_count[user.username] = count

    # print('notification user', notification_count)
