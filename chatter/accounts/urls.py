from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register , name='register'),
    path('login', views.login , name='login'),
    path('logout', views.logout , name='logout'),
    path('contacts', views.contacts , name='contacts'),
    path('add_contacts', views.add_contacts , name='add_contacts'),
    path('add_contact', views.add_contact , name='add_contact'),
]
