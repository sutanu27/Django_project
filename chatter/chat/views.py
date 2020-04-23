from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Contacts
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import viewsets, generics
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.
@login_required(login_url='')
def chat(request):
    usr=request.user
    chatrooms=[]
    for Chatroom in ChatRoom.objects.filter(roomie=usr):
        guest_name=Chatroom.guest_name(usr)
        img_link=Chatroom.room_image(usr)
        link=Chatroom.id
        chatrooms.append({
            'link':link,
            'name':guest_name,
            'timestamp':Chatroom.lastping.strftime('%Y-%m-%d %H:%M'),
            'img_link': img_link
        })
    Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'], reverse = True)
    return render(request,'chat.html',{'chatrooms': Chatrooms})

@login_required(login_url='/')
def chatroom(request, room_id):
    room=ChatRoom.objects.filter(id=room_id,roomie=request.user)
    if room.exists():
        return render(request,'chatroom.html',{'room_id':room_id, 'room_type':room.first().group, 'room_name':room.first().guest_name(request.user) })
    else:
        raise PermissionDenied("You do not have permission")


def get_create_room(user1,user2):
    chatroom1=user1.roommate.filter(group=False)
    chatroom2=user2.roommate.filter(group=False)
    chatroom=set(chatroom2).intersection(chatroom1)
    if chatroom!=set():
        return chatroom.pop()
    else:
        Chatroom=ChatRoom.objects.create(group=False)
        Chatroom.roomie.add(user1,user2)
        Chatroom.save()
        return Chatroom

@login_required(login_url='/')
def get_or_create_room(request,username):
    user1=request.user
    user2=User.objects.filter(username=username).first()
    chatroom=get_create_room(user1=user1,user2=user2)
    return redirect('chatroom',room_id=chatroom.id)

@login_required(login_url='/')
def search_name(request):
    if request.method == 'GET':
        username_substring=request.GET['username_substring']
        users=[]
        for user in User.objects.filter(username__icontains=username_substring).exclude(username=request.user.username):
            img_link=user.profile.profile_image.url
            users.append({
                'full_name': user.first_name+' '+user.last_name,
                'username': user.username,
                'img_link': img_link
            }
            )
        return render(request,'search.html',{'users':users})
    else :
        return redirect('search')

@login_required(login_url='/')
def search(request):
        return render(request,'search.html',{'users':[]})


# class ChatRoomView(generics.ListAPIView):
#     serializer_class=ChatRoomSerializer

#     def get_queryset(self):
#         queryset=ChatRoom.objects.all()
#         host=self.request.query_params.get("host",'')
#         if host:
#             host_user=User.objects.get(username=host)
#             return queryset.filter(roomie=host_user)
#         return queryset



@login_required(login_url='/')
def chatroomMessageViewApi(request):
    roomid=request.GET['roomid']
    messages=[]
    if roomid:
        room=ChatRoom.objects.filter(id=roomid).first()
        for msg in room.messages:
            is_send=False
            file_url=''
            auther_name=msg.auther.username
            if auther_name==request.user.username:
                is_send=True
            else:
                c_name=request.user.host.filter(username=auther_name).first()
                if c_name:
                    auther_name=c_name.full_name
            if msg.file_msg:
                file_url=msg.file_msg.url
            messages.append({
                "content":msg.content,
                "file_msg_link":file_url,
                "time_stamp":msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                "auther_name":auther_name,
                "is_send": is_send
            })

    serializer=MessagesChatroomSerializer(messages,many=True)
    return JsonResponse(serializer.data, safe=False)

def jsonify_room(Chatroom,usr):
    guest_name=Chatroom.guest_name(usr)
    img_link=Chatroom.room_image(usr)
    link=Chatroom.id
    return {
        'link':link,
        'name':guest_name,
        'timestamp':Chatroom.lastping.strftime('%Y-%m-%d %H:%M'),
        'img_link': img_link,
        'is_group':Chatroom.group
        }



@login_required(login_url='/')
def chatRoomsApi(request,username=''):
    usr=request.user
    if username:
        user2=User.objects.filter(username=username).first()
        chatroom=get_create_room(user1=usr,user2=user2)
        serializer=ChatRoomSerializer(jsonify_room(chatroom,usr))
        return JsonResponse(serializer.data, safe=False)

    chatrooms=[ jsonify_room(Chatroom,usr)  for Chatroom in ChatRoom.objects.filter(roomie=usr)]
    Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'], reverse = True)
    serializer=ChatRoomSerializer(Chatrooms,many=True)
    return JsonResponse(serializer.data, safe=False)

class messagesViewsets(viewsets.ModelViewSet):
    queryset=messages.objects.all()
    serializer_class=messagesSerializer

class chatroomsViewsets(viewsets.ModelViewSet):
    queryset=ChatRoom.objects.all()
    serializer_class=ChatRoomSerializer
