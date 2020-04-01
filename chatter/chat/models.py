from django.db import models
from accounts.models import Contacts
from django.contrib.auth.models import auth, User
from django.contrib import admin
from django.utils import timezone
import uuid 

# Create your models here.


class ChatRoom(models.Model):
    roomie=models.ManyToManyField(User,related_name='roommate', symmetrical=True,)
    group=models.BooleanField()	
    group_name=models.TextField(null=True,blank=True)
    create_datetime=models.DateTimeField(auto_now_add=True)

    @property
    def lastping(self):
        msg=messages.objects.filter(room=self).order_by('-timestamp')
        if msg.exists():
            return msg.first().timestamp
        else:
            return self.create_datetime

    def guest_name(self,user):
        if self.group:
            return self.group_name
        else:
            guest=self.roomie.exclude(username=user.username).first()
            contact=Contacts.objects.filter(host=user,username=guest.username)
            if contact.exists():
                return contact.first().first_name+' '+contact.first().last_name
            else:
                return guest.username
        
    def __str__(self):
        return str(self.id)

 

admin.site.register(ChatRoom)

class messages(models.Model):
    auther=models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg')
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    room=models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room')

    def __str__(self):
        return str(self.room.id)+str(self.timestamp)

admin.site.register(messages)