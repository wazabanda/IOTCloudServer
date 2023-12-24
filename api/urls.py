from django.contrib import admin
from django.urls import path,include
from .views import AddNumericalLog,GetDevice

urlpatterns = [
    path('numerical-logs/<uuid:uuid>',AddNumericalLog.as_view(),name='Logs-API'),
    path('devices/<uuid:uuid>',GetDevice.as_view(),name='Logs-API'),

]
