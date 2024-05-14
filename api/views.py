from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, viewsets
from django.db.models import Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
#importing models
from .serializers import *
from core.models import *
from rest_framework.permissions import AllowAny
# Create your views here.


class GetDevice(APIView):
    
    def get_queryset(self):
        return Device.objects.none()
    
    
    def get(self,request,uuid):
        try:
            device = Device.objects.filter(device_id=uuid)[0]
            ser = DeviceSerializer(device,many=False)
            data = ser.data
            data['id'] = device.id
            return Response(data)
        except Exception as e:
            return Response({'Message':f"No logs \n{e}"})
            
        

class AddNumericalLog(APIView):
    authentication_classes = []
    permission_classes = [AllowAny] 
    def get_queryset(self):
        
        return NumericalLog.objects.all()
    
    def get(self,request,uuid):
        try:
            device = Device.objects.filter(device_id=uuid)[0]
            logs = NumericalLog.objects.filter(device=device)
            serializer = NumericalLogSerializer(logs,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Message':f"No logs \n{e}"})
        
    def post(self,request,uuid):
        data = request.data['logs']
        device = Device.objects.filter(device_id=uuid)[0]
        print(data)
        for dat in data:
            dat['device'] = device.id
            
        print(data)
        ser = NumericalLogSerializer(data=data,many=True)
   
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        print(ser.errors)
        print(ser.error_messages)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LocationDataAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        try:
            device = Device.objects.get(device_id=uuid)
            location_data = LocationData.objects.filter(device=device)
            serializer = LocationSerilizer(location_data, many=True)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response({'Message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Message': f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, uuid):
        try:
            device = Device.objects.get(device_id=uuid)
            data = request.data
            data['device'] = device.id
            serializer = LocationSerilizer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({'Message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Message': f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)