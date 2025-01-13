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



from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Device
# from core.forms import DeviceForm

class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'devices/device_form.html'
    success_url = reverse_lazy('device_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Device created successfully!')
        return super().form_valid(form)

class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'devices/device_form.html'
    success_url = reverse_lazy('device_list')

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Device updated successfully!')
        return super().form_valid(form)

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    template_name = 'devices/device_confirm_delete.html'
    success_url = reverse_lazy('device_list')

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Device deleted successfully!')
        return super().delete(request, *args, **kwargs)
