from django.urls import path, include
from .views import *
from rest_framework import routers

router=routers.DefaultRouter()
router.register('',messagesViewsets)
router.register('',chatroomsViewsets)

urlpatterns = [
    path('ChatRoom/<str:username>', chatRoomsApi),
    path('chatroomapi/', include(router.urls)),
    path('ChatRoom/', chatRoomsApi),
    path('messages/', chatroomMessageViewApi),
    path('messagesapi/', include(router.urls)),
    ]