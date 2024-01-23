from django.db import models
from chatapp.models import User


class Chat(models.Model):
    sender = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,)
    message = models.TextField(null=True, blank=True)
    theard_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.message}"



class Notificaton(models.Model):
    message = models.ForeignKey(to=Chat, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True) #sender create the notification and here user is reciver to collect message
    is_seen = models.BooleanField(default=False) 

    def __str__(self) -> str:
        return f"{self.user}"
    

