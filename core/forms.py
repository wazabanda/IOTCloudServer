from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name']
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-input px-4 py-3 rounded-full'})
        }
