from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name','owner','device_id']
     


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['owner','key']


@admin.register(NumericalLog)
class NumericalLogAdmin(admin.ModelAdmin):
    list_display = ['device','value','date_time','data_label']
    list_editable = ['data_label','date_time'] 
    
    
@admin.register(GPIOOutputPin)
class GPIOPinAdmin(admin.ModelAdmin):
    list_display = ['name','pin','device']