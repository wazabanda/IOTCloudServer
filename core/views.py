from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from Mqttapp.mqtt_thread import start_mqtt_client
from .models import Device,ApiKey,NumericalLog,GPIOOutputPin,LocationData, ProfileSettings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import GPIOPinForm, UserProfileForm, ProfileSettingsForm, ApiKeyForm
from .mixins import DeviceOwnershipMixin, GPIOPinOwnershipMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
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

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # Get user profile data
        try:
            profile_settings = ProfileSettings.objects.get(user=request.user)
        except ProfileSettings.DoesNotExist:
            profile_settings = ProfileSettings.objects.create(user=request.user)
        
        # Get API keys
        api_keys = ApiKey.objects.filter(owner=request.user)
        
        # Get device statistics
        devices = Device.objects.filter(owner=request.user)
        total_devices = devices.count()
        active_devices = devices.filter(is_active=True).count()
        
        # Prepare forms
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileSettingsForm(instance=profile_settings)
        password_form = PasswordChangeForm(request.user)
        api_key_form = ApiKeyForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'api_key_form': api_key_form,
            'api_keys': api_keys,
            'stats': {
                'total_devices': total_devices,
                'active_devices': active_devices,
            }
        }
        
        return render(request, 'core/profile.html', context)
    
    def post(self, request):
        form_type = request.POST.get('form_type')
        
        if form_type == 'user_profile':
            user_form = UserProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        elif form_type == 'profile_settings':
            try:
                profile_settings = ProfileSettings.objects.get(user=request.user)
            except ProfileSettings.DoesNotExist:
                profile_settings = ProfileSettings(user=request.user)
            
            profile_form = ProfileSettingsForm(request.POST, instance=profile_settings)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your settings have been updated.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        elif form_type == 'password_change':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been updated.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        elif form_type == 'api_key':
            api_key_form = ApiKeyForm(request.POST)
            if api_key_form.is_valid():
                api_key = api_key_form.save(commit=False)
                api_key.owner = request.user
                api_key.save()
                messages.success(request, 'New API key has been created.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        # If we get here, there was an error, so re-render the page with the appropriate form
        return self.get(request)
