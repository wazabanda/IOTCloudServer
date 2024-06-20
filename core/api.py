from ninja import Router, Schema
from ninja.errors import HttpError
from typing import List, Dict
from core.models import Device, NumericalLog, LocationData
from django.shortcuts import get_object_or_404
from .schema import DeviceSchema, NumericalLogSchema, LocationDataSchema
from datetime import datetime

router = Router(tags=['Devices'])



@router.get("/devices", response=List[DeviceSchema])
def list_devices(request):
    devices = Device.objects.all()
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
    date_time: datetime
    data_label: str

class AddNumericalLogPayload(Schema):
    logs: List[LogEntry]

@router.get("/numerical-logs/{uuid}", response=List[NumericalLogSchema])
def get_numerical_logs(request, uuid: str):
    device = get_object_or_404(Device, device_id=uuid)
    logs = NumericalLog.objects.filter(device=device)
    return logs

@router.post("/numerical-logs/{uuid}", response=List[NumericalLogSchema])
def add_numerical_log(request, uuid: str, payload: AddNumericalLogPayload):
    device = get_object_or_404(Device, device_id=uuid)
    logs = payload.logs
    log_objects = []
    for log in logs:
        log_objects.append(NumericalLog(device=device, **log.dict()))
    NumericalLog.objects.bulk_create(log_objects)
    return log_objects

@router.get("/location-data/{uuid}", response=List[LocationDataSchema])
def get_location_data(request, uuid: str):
    device = get_object_or_404(Device, device_id=uuid)
    location_data = LocationData.objects.filter(device=device)
    return location_data

@router.post("/location-data/{uuid}", response=LocationDataSchema)
def add_location_data(request, uuid: str, payload: LocationDataSchema):
    device = get_object_or_404(Device, device_id=uuid)
    location_data = LocationData.objects.create(device=device, **payload.dict())
    return location_data

