from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Device, GPIOOutputPin

class DeviceOwnershipMixin(LoginRequiredMixin):
    """
    Mixin to verify that the user owns the device they're trying to access.
    """
    def dispatch(self, request, *args, **kwargs):
        # First check if user is logged in via LoginRequiredMixin
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # If we have a device_id in kwargs, verify ownership
        if 'pk' in kwargs:
            device = get_object_or_404(Device, pk=kwargs['pk'])
            if device.owner != request.user:
                return HttpResponseForbidden("You don't have permission to access this device.")
        
        # If we have a uuid in kwargs, verify ownership
        if 'uuid' in kwargs:
            device = get_object_or_404(Device, device_id=kwargs['uuid'])
            if device.owner != request.user:
                return HttpResponseForbidden("You don't have permission to access this device.")
                
        return super().dispatch(request, *args, **kwargs)

class GPIOPinOwnershipMixin(LoginRequiredMixin):
    """
    Mixin to verify that the user owns the device associated with a GPIO pin.
    """
    def dispatch(self, request, *args, **kwargs):
        # First check if user is logged in via LoginRequiredMixin
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # If we have a pin_id in kwargs, verify ownership of associated device
        if 'pk' in kwargs:
            gpio_pin = get_object_or_404(GPIOOutputPin, pk=kwargs['pk'])
            if gpio_pin.device.owner != request.user:
                return HttpResponseForbidden("You don't have permission to access this GPIO pin.")
                
        return super().dispatch(request, *args, **kwargs) 