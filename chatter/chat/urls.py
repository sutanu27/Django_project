from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chat , name='chat'),
    path('<str:room_name>/', views.chatroom , name='chatroom')
]
