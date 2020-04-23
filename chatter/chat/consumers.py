from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import messages, ChatRoom
from django.core.files import File

class ChatConsumer(AsyncWebsocketConsumer):

    async def add_new_msg(self, data):
        msg=data['message_content']
        user=self.scope["user"]
        is_file=data['is_file']
        msg_inst=messages.objects.create(auther=user,content=msg,room=self.chatroom)
        # Send message to room group
        return await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.josonify(msg_inst),
                'has_file': is_file
            }
        )

    def josonify( self, msg_inst):
        return{
            'id':msg_inst.id,
            'auther': msg_inst.auther.username,
            'content': msg_inst.content,
            'file_msg_url':  msg_inst.file_msg.url if msg_inst.file_msg else '',
            'timestamp': msg_inst.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        json_msgs={
            'has_file':event['has_file'],
            'message': event['message']
        }
        await self.send(text_data=json.dumps(json_msgs))


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chatroom=ChatRoom.objects.get(id=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data,bytes_data=None):
        text_data_json = json.loads(text_data)
        await self.add_new_msg(data=text_data_json)

