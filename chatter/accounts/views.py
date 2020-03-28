from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Contacts
from chat.models import ChatRoom

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1!=password2 :
            messages.info(request,"Password doesn't match.")
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,"User Name is taken. Please try some other name.")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"This E-mail id is already in use. Please try something else.")
            return redirect('register')
        else :
            User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
            return redirect('/')
    else :
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.info(request,"User Name doesn't exists.")
            return redirect('login')
        else:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.error(request,'Username or password invallid')
                return redirect('login')
    else:
        return render(request,'login.html')

def logout(request) :
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/accounts/login')
def contacts(request) :
    contacts=Contacts.objects.filter(host=request.user).order_by('first_name','last_name')
    return render(request,'contacts.html',{'contacts':contacts})

@login_required(login_url='/accounts/login')
def add_contacts(request) :
    return render(request,'add_contact.html')

@login_required(login_url='/accounts/login')
def add_contact(request) :
    if request.method == 'GET':
        first_name=request.GET['first_name']
        last_name=request.GET['last_name']
        username=request.GET['username']
        if User.objects.filter(username=username).exists():
            Contacts.objects.create(host=request.user, first_name=first_name, last_name=last_name, username=username)
            return redirect('contacts')
        else:
            messages.info(request,"User Name doesn't exits.")   
            return redirect('add_contacts')
    else:
        return redirect('contacts')

@login_required(login_url='/accounts/login')
def create_group(request):
    contacts=Contacts.objects.filter(host=request.user).order_by('first_name','last_name')
    return render(request,'create_group.html',{'contacts':contacts})

@login_required(login_url='/accounts/login')
def add_group(request):
    if request.method == 'POST':
        group_name=request.POST['group_name']
        contacts=request.POST.getlist('contact[]')
        print(str(contacts))
        Chatroom=ChatRoom.objects.create(group=True,group_name=group_name)
        Chatroom.roomie.add(request.user)
        for contact in contacts:
            user=User.objects.get(username=contact)
            Chatroom.roomie.add(user)
        Chatroom.save()
        return render(request,'home.html')
    else:
        return redirect('contacts')
