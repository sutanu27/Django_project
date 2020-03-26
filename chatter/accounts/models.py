from django.db import models
from django.contrib.auth.models import auth, User
from django.contrib import admin

# Create your models here.
class Contacts(models.Model):
    host=models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    first_name=models.TextField()
    last_name=models.TextField()
    username=models.TextField()
    
    def __str__(self):
        return self.username

admin.site.register(Contacts)

