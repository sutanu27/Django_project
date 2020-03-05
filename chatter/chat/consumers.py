from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import message

class ChatConsumer(AsyncWebsocketConsumer):
    invoke = {
        'load_old_msg' : load_old_msg ,
        'add_new_msg': add_new_msg 
        }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.invoke[text_data_json['invoke_fn']](self , text_data_json)

    async def add_new_msg(self, data):
        msg=json.loads(data)['msg_content']
        user=self.scope["user"]
        msg_inst=message.objects.create(auther=user,content=msg)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'auther': msg_inst.username,
                'content': msg_inst.content,
                'timestamp': msg_inst.timestamp
            }
        )


    async def load_old_msg(self , data):
        messages=message.objects.all().order_by('-timestamp')
        json_msg=[ self.josonify(msg_inst=msg) for msg in messages ]
        return self.send(text_data=json_msg)

    def josonify(self, msg_inst):
        msg_json={
            'auther': msg_inst.username,
            'content': msg_inst.content,
            'timestamp': msg_inst.timestamp
        }
        return msg_json


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))