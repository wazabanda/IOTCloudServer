from ninja import Schema,ModelSchema
from typing import List, Optional
from datetime import datetime
import uuid
from .models import *


class DeviceSchema(ModelSchema):
    class Config:
        model = Device
        model_fields = ["device_name", "owner", "device_id"]

class NumericalLogSchema(ModelSchema):
    class Config:
        model = NumericalLog
        model_fields = ["value", "data_label"]

class NumericalLogOutSchema(ModelSchema):
    class Config:
        model = NumericalLog
        model_fields = ["value", "data_label",'date_time']
        
class GpioSchema(ModelSchema):
    class Config:
        model = GPIOOutputPin
        model_fields = ['name',"pin","device"]


class LocationDataSchema(ModelSchema):
    class Config:
        model = LocationData
        model_fields = "__all__" 



class InventoryEntryLogSchema(ModelSchema):
    class Config:
        model = InventoryEntryLog
        model_fields = ['log_type','timestamp']


class InventoryEntryOutSchema(ModelSchema):
    class Config:
        model = InventoryEntry 
        model_fields = "__all__"


class InventoryEntryInSchema(Schema):
    device:str
    logs:InventoryEntryLogSchema
