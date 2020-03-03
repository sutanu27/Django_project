from django.shortcuts import render 

# Create your views here.
def chat(request):
    return render(request,'chat.html')

def chatroom(request, room_name):
    return render(request,'chatroom.html',{'room_name':room_name})