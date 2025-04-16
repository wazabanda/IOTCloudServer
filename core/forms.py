from django import forms
from .models import Device, GPIOOutputPin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.contrib.auth.models import User
from .models import ProfileSettings, ApiKey
from django.utils import timezone

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name','is_active']
        
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name', css_class='input input-bordered w-full'),
            Field('last_name', css_class='input input-bordered w-full'),
            Field('email', css_class='input input-bordered w-full'),
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input input-bordered w-full'})

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = ProfileSettings
        fields = ['google_api_key']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('google_api_key', css_class='input input-bordered w-full'),
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input input-bordered w-full'})

class ApiKeyForm(forms.ModelForm):
    expiry_days = forms.IntegerField(
        min_value=1, 
        max_value=365, 
        initial=30,
        label="Expiry (days)",
        required=False,
    )
    
    never_expires = forms.BooleanField(
        required=False,
        label="Never Expires",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'})
    )
    
    class Meta:
        model = ApiKey
        fields = ['expiry_days', 'never_expires']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('expiry_days', css_class='input input-bordered w-full'),
            Field('never_expires', css_class='checkbox'),
        )
        self.fields['expiry_days'].widget.attrs.update({'class': 'input input-bordered w-full'})
        
    def clean(self):
        cleaned_data = super().clean()
        never_expires = cleaned_data.get('never_expires')
        expiry_days = cleaned_data.get('expiry_days')
        
        if never_expires and expiry_days:
            # If "never expires" is checked, we don't need expiry_days
            self.add_error('expiry_days', 'This field should be empty if "Never Expires" is checked.')
        elif not never_expires and not expiry_days:
            # If "never expires" is not checked, we need expiry_days
            self.add_error('expiry_days', 'Please specify expiry days or check "Never Expires".')
            
        return cleaned_data
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set expiry date based on form data
        if self.cleaned_data.get('never_expires'):
            # Set to a far future date (e.g., 100 years from now)
            instance.expiry = timezone.now() + timezone.timedelta(days=36500)  # ~100 years
        else:
            days = self.cleaned_data.get('expiry_days', 30)
            instance.expiry = timezone.now() + timezone.timedelta(days=days)
        
        if commit:
            instance.save()
        return instance
