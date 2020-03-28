from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Contacts
from .models import ChatRoom
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/accounts/login')
def chat(request):
    usr=request.user
    chatrooms=[]
    for Chatroom in ChatRoom.objects.filter(roomie=usr):
        guest_name=Chatroom.guest_name(usr)
        link=Chatroom.id
        chatrooms.append({
            'link':link,
            'name':guest_name,
            'timestamp':Chatroom.lastping
        })
        print(guest_name)
    Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'], reverse = True)
    return render(request,'chat.html',{'chatrooms': Chatrooms})

@login_required(login_url='/accounts/login')
def chatroom(request, room_id):
    room=ChatRoom.objects.filter(id=room_id,roomie=request.user)
    if room.exists():
        return render(request,'chatroom.html',{'room_name':room_id})
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

@login_required(login_url='/accounts/login')
def get_or_create_room(request,username):
    user1=request.user
    user2=User.objects.filter(username=username).first()
    chatroom=get_create_room(user1=user1,user2=user2)
    return redirect('chatroom',room_id=chatroom.id)

@login_required(login_url='/accounts/login')
def search_name(request):
    if request.method == 'GET':
        username_substring=request.GET['username_substring']
        users=[ {'name':user.username} for user in User.objects.filter(username__icontains=username_substring).exclude(username=request.user.username)]
        return render(request,'search.html',{'users':users})
    else :
        return redirect('search')

@login_required(login_url='/accounts/login')
def search(request):
        return render(request,'search.html',{'users':[]})


