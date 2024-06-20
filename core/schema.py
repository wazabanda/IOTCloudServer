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
        model_fields = ["device", "value", "date_time", "data_label"]

class LocationDataSchema(ModelSchema):
    class Config:
        model = LocationData
        model_fields = "__all__" 