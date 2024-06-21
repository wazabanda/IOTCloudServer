from django.contrib import admin
from django.urls import path,include
from .views import HomeView,DeviceData

urlpatterns = [
    path('',HomeView.as_view(),name='home-view'),
    path('accounts/profile/',HomeView.as_view(),name='Profile-view'),
    
    path('devices/<uuid:uuid>/',DeviceData.as_view(),name='device')
]
