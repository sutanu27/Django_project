from django.db import models
from accounts.models import Contacts
from django.contrib.auth.models import auth, User
from django.contrib import admin
from datetime import datetime
import uuid 

# Create your models here.


class ChatRoom(models.Model):
    user1=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def lastping(self):
        msg=messages.objects.filter(room=self).order_by('timestamp')
        if msg.exists():
            return msg.first().timestamp
        else:
            return datetime.now()

    @property
    def name(self):
        return self.id

    def guest_name(self,user):
        if user==self.user1:
            host=self.user1
            guest=self.user2
        elif user==self.user2:
            host=self.user2
            guest=self.user1
        else:
            return ''
        contact=Contacts.objects.filter(host=host,username=guest.username)
        if contact.exists():
            return contact.first().first_name+' '+contact.first().last_name
        else:
            return guest.username
        

    def __str__(self):
        return str(self.name)

 

admin.site.register(ChatRoom)

class messages(models.Model):
    auther=models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg')
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    room=models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room')

    def __str__(self):
        return str(self.room.id)+str(self.timestamp)

admin.site.register(messages)