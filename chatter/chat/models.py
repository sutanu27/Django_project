from django.db import models
from django.contrib.auth.models import auth, User
from django.contrib import admin

# Create your models here.

class messages(models.Model):
    auther=models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg')
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

admin.site.register(messages)