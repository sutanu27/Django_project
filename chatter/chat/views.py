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
    for Chatroom in ChatRoom.objects.filter( Q(user1=usr) | Q(user2=usr)):
        if Chatroom.user1==usr:
            guest_name=Chatroom.guest_name(Chatroom.user1)
        else:
            guest_name=Chatroom.guest_name(Chatroom.user2)
        link=Chatroom.id
        chatrooms.append({
            'link':link,
            'name':guest_name,
            'timestamp':Chatroom.lastping
        })
        Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'],reverse = True)
    return render(request,'chat.html',{'chatrooms':Chatrooms})

@login_required(login_url='/accounts/login')
def chatroom(request, room_name):
    room=ChatRoom.objects.filter(id=room_name).first()
    if ( request.user==room.user1 or request.user==room.user2):
        return render(request,'chatroom.html',{'room_name':room_name})
    else:
        raise PermissionDenied("You do not have permission")


def get_create_room(user1,user2):
    chatroom=ChatRoom.objects.filter(user1=user1,user2=user2)
    if chatroom.exists():
        return chatroom.first()
    else:
        chatroom=ChatRoom.objects.filter(user1=user2,user2=user1)
        if chatroom.exists():
            return chatroom.first()
        else:
            return ChatRoom.objects.create(user1=user1, user2=user2)

@login_required(login_url='/accounts/login')
def get_or_create_room(request,username):
    user1=request.user
    user2=User.objects.filter(username=username).first()
    chatroom=get_create_room(user1=user1,user2=user2)
    return redirect('chatroom',room_name=chatroom.name)

@login_required(login_url='/accounts/login')
def search_name(request):
    if request.method == 'POST':
        username_substring=request.POST['username_substring']
        users=[]
        for user2 in User.objects.filter(username__icontains=username_substring).exclude(username=request.user.username):
            link=get_create_room(request.user,user2).id
            name=user2.username
            users.append({
                'link':link,
                'name':name
            })
        return render(request,'search.html',{'users':users})
    else :
        return redirect('search')

@login_required(login_url='/accounts/login')
def search(request):
        return render(request,'search.html',{'users':[]})


