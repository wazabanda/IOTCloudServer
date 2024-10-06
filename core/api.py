from core.admin import DeviceAdmin
from ninja import Router, Schema
from ninja.errors import HttpError
from typing import List, Dict
from core.models import Device, GPIOOutputPin, NumericalLog, LocationData
from django.shortcuts import get_object_or_404
from .schema import * 
from datetime import datetime

router = Router(tags=['Device API'])



@router.get("/devices", response=List[DeviceSchema])
def list_devices(request):
    print(request.auth.id)
    devices = Device.objects.filter(owner__id=request.auth.id)
    return devices

@router.get("/device/{uuid}", response=DeviceSchema)
def get_device(request, uuid: str):
    try:
        device = Device.objects.get(device_id=uuid)
        return device
    except Device.DoesNotExist:
        raise HttpError(404, f"No device found with id {uuid}")

class LogEntry(Schema):
    value: float
    # date_time: datetime
    data_label: str

class AddNumericalLogPayload(Schema):
    logs: List[LogEntry]

@router.get("/device_logs/{uuid}",auth=None, response=List[NumericalLogOutSchema])
def get_numerical_logs(request, uuid: str):
    # print("here")
    device = Device.objects.get(device_id=uuid)
    print(device)
    logs = NumericalLog.objects.filter(device=device)
    # print(logs)
    return logs


@router.post("/numerical-logs/{uuid}",auth=None, response=List[NumericalLogSchema])
def add_numerical_log(request, uuid: str, payload: AddNumericalLogPayload):
    device = get_object_or_404(Device, device_id=uuid)
    logs = payload.logs
    log_objects = []
    for log in logs:
        log_objects.append(NumericalLog(device=device, **log.dict()))
    NumericalLog.objects.bulk_create(log_objects)
    return log_objects

@router.get("/location-data/{uuid}",auth=None, response=List[LocationDataSchema])
def get_location_data(request, uuid: str):
    device = get_object_or_404(Device, device_id=uuid)
    location_data = LocationData.objects.filter(device=device)
    return location_data

@router.post("/location-data/{uuid}",auth=None, response=LocationDataSchema)
def add_location_data(request, uuid: str, payload: LocationDataSchema):
    device = get_object_or_404(Device, device_id=uuid)
    location_data = LocationData.objects.create(device=device, **payload.dict())
    return location_data
0
@router.get("/pins/{uuid}",auth=None,response=List[GpioSchema])
def get_pins(request,uuid:str):
    device = get_object_or_404(Device,device_id=uuid)
    pins = GPIOOutputPin.objects.filter(device=device)

    return pins

@router.get("/inventory/entry/{uuid}",auth=None,response=List[InventoryEntryOutSchema])
def get_inventory_entry(request,uuid:str):
    device = get_object_or_404(Device,device_id=uuid)
    inventory_entry = InventoryEntry.objects.filter(device=device)
    return inventory_entry

@router.get("/inventory/logs/{id}",auth=None,response=List[InventoryEntryLogSchema])
def get_inventory_log(request,id:str):
    inventory_entry = InventoryEntry.objects.filter(entry_id=id)[0]
    logs = InventoryEntryLog.objects.filter(parent_entry=inventory_entry)
    return logs


@router.post("/inventory/logs/{id}",auth=None,response=List[InventoryEntryLogSchema])
def create_inventory_log(request,id:str,payload:InventoryEntryLogSchema):
    inventory_entry = InventoryEntry.objects.filter(entry_id=id)[0]
    log = InventoryEntryLog.objects.create(parent_entry=inventory_entry,log_type=payload.log_type,timestamp=payload.timestamp)
    logs = InventoryEntryLog.objects.filter(parent_entry=inventory_entry)
    return logs
