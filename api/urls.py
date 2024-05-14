from django.contrib import admin
from django.urls import path,include
from .views import AddNumericalLog,GetDevice,LocationDataAPI

urlpatterns = [
    path('numerical-logs/<uuid:uuid>',AddNumericalLog.as_view(),name='Logs-API'),
     path('location/<uuid:uuid>',LocationDataAPI.as_view(),name='Location-API'),
    path('devices/<uuid:uuid>',GetDevice.as_view(),name='device-API'),

]
