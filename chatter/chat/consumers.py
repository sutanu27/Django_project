from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import messages, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):

    async def add_new_msg(self, data):
        msg=data['msg_content']
        user=self.scope["user"]
        msg_inst=messages.objects.create(auther=user,content=msg,room=self.chatroom)
        print('add_new_msg'+msg_inst.auther.username+'*'*80)
        # Send message to room group
        return await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.josonify(msg_inst)
            }
        )

    def josonify( self, msg_inst):
        return{
            'auther': msg_inst.auther.username,
            'content': msg_inst.content,
            'timestamp': str(msg_inst.timestamp)
        }
        

    async def load_old_msg(self , data):
        msgs=messages.objects.filter(room=self.chatroom).order_by('timestamp')
        list_msgs=[ self.josonify(msg_inst=msg) for msg in msgs ]
        json_msgs={
            'command':'old_messages',
            'messeges':list_msgs
            }
        print(json.dumps(json_msgs))
        await self.send(json.dumps(json_msgs))

    invoke = {
        'add_new_msg': add_new_msg ,
        'load_old_msg' : load_old_msg 
        }


    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        json_msgs={
            'command': 'new_message',
            'message': event['message']
        }
        print(json.dumps(json_msgs))
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
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['invoke_fn']=='load_old_msg':
            await self.load_old_msg(data=text_data_json)
        else:
            await self.add_new_msg(data=text_data_json)

