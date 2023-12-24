from rest_framework import serializers
from core.models import *


# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         exclude = ("contact", "status")

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_name",'owner','device_id']
        

class NumericalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericalLog
        fields = ['device','value','date_time','data_label']