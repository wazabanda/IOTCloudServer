from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Device,ApiKey,NumericalLog,GPIOOutputPin
# Create your views here.


class ProfileView(View,LoginRequiredMixin):
    
    def get(self,request):
        context = {
            "devices":Device.objects.filter(owner=request.user) if not request.user.is_anonymous else None
        }
        
        return render(request,'core/index.html',context)


class DeviceData(View,LoginRequiredMixin):
    
    def get(self,request,uuid):
        device = Device.objects.filter(device_id=uuid)[0]
        context = {
            "numerical_logs":NumericalLog.objects.filter(device=device),
            "device":device,
            "gpiopins":GPIOOutputPin.objects.filter(device=device)
        }
        
        return render(request,'core/device.html',context)