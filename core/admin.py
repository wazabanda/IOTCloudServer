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
    

@admin.register(LocationData)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['device','lat','lng']
    

@admin.register(ProfileSettings)
class ProfileSettings(admin.ModelAdmin):
    list_display=['user']
    
    
class MqttTopicInline(admin.TabularInline):
    model = MqttTopic
    extra = 1

@admin.register(MqttBrokerSettings)
class MqttBrokerSettingsAdmin(admin.ModelAdmin):
    inlines = [MqttTopicInline]
    list_display = ['name','broker_address','port','username']


class InventoryEntryLogInline(admin.TabularInline):
    model = InventoryEntryLog
    extra = 1


@admin.register(InventoryEntry)
class InventoryEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_name','entry_id']
    inlines = [InventoryEntryLogInline]
