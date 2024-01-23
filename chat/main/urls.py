from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('index/',views.index, name='index'),
    
    path('<str:username>/',views.main_chat, name='main-chat'),
]



#  {% for key, value in notification_count.items %}
#                                                 {% if user.username == key %}
#                                                     <small id="count">{{ value}}</small> 
#                                                 {% endif %}
#                                             {% endfor %}