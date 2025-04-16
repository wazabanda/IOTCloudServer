from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from Mqttapp.mqtt_thread import start_mqtt_client
from .models import Device,ApiKey,NumericalLog,GPIOOutputPin,LocationData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import GPIOPinForm
from .mixins import DeviceOwnershipMixin, GPIOPinOwnershipMixin
# Create your views here.


class HomeView(LoginRequiredMixin, View):
    
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'core/index.html', {})
            
        devices = Device.objects.filter(owner=request.user)
        
        # Calculate statistics
        total_devices = devices.count()
        active_devices = devices.filter(is_active=True).count()
        inactive_devices = total_devices - active_devices
        
        # Get the most recently updated device
        latest_device = devices.order_by('-last_seen').first()
        
        # Get recent logs
        recent_logs = NumericalLog.objects.filter(
            device__owner=request.user
        ).order_by('-date_time')[:5]
        
        context = {
            "devices": devices,
            "stats": {
                "total_devices": total_devices,
                "active_devices": active_devices,
                "inactive_devices": inactive_devices,
                "latest_device": latest_device,
            },
            "recent_logs": recent_logs
        }
        
        return render(request, 'core/index.html', context)


class DeviceData(DeviceOwnershipMixin, View):
    
    def get(self, request, uuid):
        start_mqtt_client(request.user)
        device = get_object_or_404(Device, device_id=uuid, owner=request.user)
        context = {
            "numerical_logs": NumericalLog.objects.filter(device=device),
            "has_location_data": LocationData.objects.filter(device=device).exists(),
            "device": device,
            "gpiopins": GPIOOutputPin.objects.filter(device=device)
        }
        
        return render(request, 'core/device.html', context)




class GPIOPinCreateView(DeviceOwnershipMixin, CreateView):
    model = GPIOOutputPin
    form_class = GPIOPinForm
    template_name = 'core/device/detail.html'  # This won't be used directly
    
    def form_valid(self, form):
        device = form.cleaned_data['device']
        
        # Verify the user owns this device
        if device.owner != self.request.user:
            messages.error(self.request, "You don't have permission to add pins to this device.")
            return redirect('device_list')
        
        gpio_pin = form.save()
        messages.success(self.request, f'GPIO Pin "{gpio_pin.name}" added successfully!')
        return redirect('device', pk=device.id)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error adding GPIO pin. Please check the form.")
        if 'device' in form.cleaned_data:
            return redirect('device', pk=form.cleaned_data['device'].id)
        return redirect('device_list')

class GPIOPinDeleteView(GPIOPinOwnershipMixin, DeleteView):
    model = GPIOOutputPin
    
    def get_success_url(self):
        device_id = self.object.device.id
        return reverse_lazy('device', kwargs={'pk': device_id})
    
    def delete(self, request, *args, **kwargs):
        gpio_pin = self.get_object()
        device_id = gpio_pin.device.id
        messages.success(request, f'GPIO Pin "{gpio_pin.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)
