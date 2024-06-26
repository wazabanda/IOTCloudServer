from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Mqttapp.mqtt_thread import start_mqtt_client
from .models import Device,ApiKey,NumericalLog,GPIOOutputPin,LocationData
# Create your views here.


class HomeView(LoginRequiredMixin,View):
    
    def get(self,request):
        context = {
            "devices":Device.objects.filter(owner=request.user) if not request.user.is_anonymous else None
        }
        
        return render(request,'core/index.html',context)


class DeviceData(LoginRequiredMixin,View):
    
    def get(self,request,uuid):
        start_mqtt_client(request.user)
        device = Device.objects.filter(device_id=uuid)[0]
        context = {
            "numerical_logs":NumericalLog.objects.filter(device=device),
            "has_location_data": LocationData.objects.filter(device=device).exists(),
            "device":device,
            "gpiopins":GPIOOutputPin.objects.filter(device=device)
        }
        
        return render(request,'core/device.html',context)