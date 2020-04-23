from rest_framework import serializers
from .models import *

class ContactsSerializer(serializers.Serializer):
    username=serializers.DateTimeField()
    full_name=serializers.CharField()
    img_link=serializers.CharField()


