from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Mqttapp.mqtt_thread import start_mqtt_client
from .models import Device,ApiKey, InventoryEntry,NumericalLog,GPIOOutputPin,LocationData,InventoryEntryLog
# Create your views here.


class HomeView(LoginRequiredMixin,View):
    
    def get(self,request):
        context = {
            "devices":Device.objects.filter(owner=request.user) if not request.user.is_anonymous else None
        }
        
        return render(request,'core/index.html',context)


from django.db.models import Max, OuterRef, Subquery

class DeviceData(LoginRequiredMixin, View):
    
    def get(self, request, uuid):
        start_mqtt_client(request.user)
        device = Device.objects.filter(device_id=uuid).first()
        all_inventory_entries = InventoryEntry.objects.filter(device=device)
        inventory_only = all_inventory_entries.filter(entry_type="Inventory")
        attendance_only = all_inventory_entries.filter(entry_type="Attendance")

        # Calculate total in and total out for each item
        inventory_totals = {}
        for entry in inventory_only:
            total_in = InventoryEntryLog.objects.filter(parent_entry=entry, log_type='In').count()
            total_out = InventoryEntryLog.objects.filter(parent_entry=entry, log_type='Out').count()
            inventory_totals[entry.entry_name] = {
                'total_in': total_in,
                'total_out': total_out
            }

        # Prepare attendance entries with last in and last out
        attendance_entries = []
        for entry in attendance_only:
            last_in = InventoryEntryLog.objects.filter(parent_entry=entry, log_type='In').order_by('-timestamp').first()
            last_out = InventoryEntryLog.objects.filter(parent_entry=entry, log_type='Out').order_by('-timestamp').first()
            attendance_entries.append({
                'entry_name': entry.entry_name,
                'last_in': last_in,
                'last_out': last_out,
            })

        context = {
            "numerical_logs": NumericalLog.objects.filter(device=device),
            "has_location_data": LocationData.objects.filter(device=device).exists(),
            "device": device,
            "gpiopins": GPIOOutputPin.objects.filter(device=device),
            "inventory_totals": inventory_totals,
            "attendance_entries": attendance_entries,
        }

        print(context)
        
        return render(request, 'core/device.html', context)

