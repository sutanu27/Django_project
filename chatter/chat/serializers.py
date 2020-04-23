from rest_framework import serializers
from .models import *
from chatter.serializers import *

class ChatRoomSerializer(serializers.Serializer):
    link=serializers.CharField()
    timestamp=serializers.DateTimeField()
    name=serializers.CharField()
    img_link=serializers.CharField()
    is_group=serializers.BooleanField()

class MessagesChatroomSerializer(serializers.Serializer):
    auther_name=serializers.CharField()
    is_send=serializers.BooleanField()
    time_stamp=serializers.DateTimeField()
    content=serializers.CharField()
    file_msg_link=serializers.CharField()

class ChatRoomSerializer(serializers.Serializer):
    roomie=UserSerializer(many=True)
    class Meta:
        model=ChatRoom
        fields='__all__'

class messagesSerializer(serializers.HyperlinkedModelSerializer):
    auther=UserSerializer(many=True)
    class Meta:
        model=messages
        fields='__all__'
