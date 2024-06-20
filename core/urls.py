from django.contrib import admin
from django.urls import path,include
from .views import ProfileView,DeviceData

urlpatterns = [
    path('',ProfileView.as_view(),name='Profile-view'),
    path('accounts/profile/',ProfileView.as_view(),name='Profile-view'),
    
    path('devices/<uuid:uuid>/',DeviceData.as_view(),name='device')
]
