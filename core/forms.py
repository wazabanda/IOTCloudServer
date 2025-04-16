from django import forms
from .models import Device, GPIOOutputPin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'))
        self.helper.layout = Layout(
            Field('device_name', css_class='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
        )

class GPIOPinForm(forms.ModelForm):
    class Meta:
        model = GPIOOutputPin
        fields = ['name', 'pin', 'device']
        widgets = {
            'device': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'add_gpio_pin'
        self.helper.add_input(Submit('submit', 'Add Pin', css_class='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded'))
        self.helper.layout = Layout(
            Field('name', css_class='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
            Field('pin', css_class='w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
            Field('device'),
        )
