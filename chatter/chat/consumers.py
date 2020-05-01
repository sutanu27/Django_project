from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import messages, ChatRoom
from django.core.files import File
from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):

    async def add_new_msg(self, data):
        msg=data['message_content']
        user=self.scope["user"]
        is_file=data["is_file"]
        msg_inst=messages.objects.create(auther=user,content=msg,room=self.chatroom)
        if is_file:
            self.session={
                'file_name':data["file_name"],
                'file_size':data["file_size"],
                'upload_status':data["upload_status"],
                'messege_id':msg_inst.id
            }
            # Send message to room group
        else:
            return await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': self.josonify(msg_inst),
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

    async def uploadFile(self,file_content):
        try:
            msg_inst=messages.objects.get(id=self.session['messege_id'])
            file_name=self.session['file_name']
            content=ContentFile(file_content)
            msg_inst.file_msg.save(file_name,content,save=True)
            self.session={}
            return await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': self.josonify(msg_inst),
                }
            )
        except:
            print('got an error')

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            print(text_data)
            await self.add_new_msg(data=text_data_json)
        if bytes_data:
            print('bytes_data')
            await self.uploadFile(file_content=bytes_data)


