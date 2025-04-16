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


class HomeView(LoginRequiredMixin,View):
    
    def get(self,request):
        context = {
            "devices":Device.objects.filter(owner=request.user) if not request.user.is_anonymous else None
        }
        
        return render(request,'core/index.html',context)


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




@login_required
def add_gpio_pin(request):
    if request.method == 'POST':
        form = GPIOPinForm(request.POST)
        if form.is_valid():
            device_id = form.cleaned_data['device'].id
            device = get_object_or_404(Device, id=device_id, owner=request.user)
            
            gpio_pin = form.save(commit=False)
            gpio_pin.device = device
            gpio_pin.save()
            
            messages.success(request, f'GPIO Pin "{gpio_pin.name}" added successfully!')
            return redirect('device_detail', pk=device_id)
    else:
        form = GPIOPinForm()
    
    return redirect('device_list')

@login_required
def delete_gpio_pin(request, pk):
    gpio_pin = get_object_or_404(GPIOOutputPin, pk=pk)
    
    # Ensure the user owns the device this pin belongs to
    if gpio_pin.device.owner != request.user:
        messages.error(request, "You don't have permission to delete this pin.")
        return redirect('device_list')
    
    device_id = gpio_pin.device.id
    gpio_pin.delete()
    messages.success(request, f'GPIO Pin deleted successfully!')
    return redirect('device_detail', pk=device_id)

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
        return redirect('device_detail', pk=device.id)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error adding GPIO pin. Please check the form.")
        if 'device' in form.cleaned_data:
            return redirect('device_detail', pk=form.cleaned_data['device'].id)
        return redirect('device_list')

class GPIOPinDeleteView(GPIOPinOwnershipMixin, DeleteView):
    model = GPIOOutputPin
    
    def get_success_url(self):
        device_id = self.object.device.id
        return reverse_lazy('device_detail', kwargs={'pk': device_id})
    
    def delete(self, request, *args, **kwargs):
        gpio_pin = self.get_object()
        device_id = gpio_pin.device.id
        messages.success(request, f'GPIO Pin "{gpio_pin.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)
