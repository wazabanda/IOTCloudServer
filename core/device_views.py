from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Device, GPIOOutputPin
from core.forms import DeviceForm, GPIOPinForm
from .mixins import DeviceOwnershipMixin

class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'core/device/list.html'
    context_object_name = 'devices'
    
    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'core/device/detail.html'
    context_object_name = 'device'
    
    def get_object(self, queryset=None):
        # Get the pk from the URL (which could be a UUID or an integer)
        pk = self.kwargs.get('pk')
        
        # Try to get the device by device_id (UUID) first
        device = get_object_or_404(Device, device_id=pk, owner=self.request.user)
        return device
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gpio_pins'] = GPIOOutputPin.objects.filter(device=self.object)
        context['gpio_form'] = GPIOPinForm(initial={'device': self.object})
        return context

class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'core/device/edit.html'
    success_url = reverse_lazy('device_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Device created successfully!')
        return super().form_valid(form)

class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'core/device/edit.html'
    
    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('device', kwargs={'pk': self.object.device_id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Device updated successfully!')
        return super().form_valid(form)

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    template_name = 'core/device/confirm_delete.html'
    success_url = reverse_lazy('device_list')
    
    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Device deleted successfully!')
        return super().delete(request, *args, **kwargs)
