from django.db import models
from django.contrib.auth.models import auth, User
# Create your models here.

class message(models.Model):
    auther=models.ForeignKey()