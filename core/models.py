from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets
from datetime import datetime,timezone
from django.utils import timezone
from django.urls import reverse, reverse_lazy as _
# Create your models here.




class ProfileSettings(models.Model):
    user = models.OneToOneField(User, verbose_name="Profile", on_delete=models.CASCADE,default=1)
    google_api_key = models.TextField("Google Maps API Key",null=True)
    # mqtt_broker = models.TextField(null=True)


class MqttBrokerSettings(models.Model):
    profile_settings = models.ForeignKey(ProfileSettings, verbose_name="profile_settings", on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    broker_address = models.CharField(max_length=255)
    port = models.IntegerField(default=1883)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class MqttTopic(models.Model):
    broker = models.ForeignKey(MqttBrokerSettings, related_name='topics', on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    
    
class Device(models.Model):      
        
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    device_name = models.CharField("name", max_length=50)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)
    device_id = models.UUIDField("Device ID",default=uuid.uuid4,unique=True,editable=False)
    def __str__(self):
        return self.device_name
    
    
class ApiKey(models.Model):


    class Meta:
        verbose_name = "Api Key"
        verbose_name_plural = "Api Keys"

    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)
    key = models.CharField("Key", max_length=64,default=secrets.token_urlsafe)
    expiry = models.DateTimeField("Expiry Date", default=timezone.now)
    def __str__(self):
        return self.owner.username


class NumericalLog(models.Model):

    class Meta:
        verbose_name = "Numerical Log"
        verbose_name_plural = "Numerical Logs"

    data_label = models.CharField("Lable", max_length=50,default="x")
    device = models.ForeignKey(Device, verbose_name=('Device'), on_delete=models.CASCADE)
    value = models.FloatField("Value",default=0)
    date_time = models.DateTimeField("Date and time", null=True, default=timezone.now)

    def __str__(self):
        return str(self.device)


class GPIOOutputPin(models.Model):

    

    class Meta:
        verbose_name = "GPIO Output Pin"
        verbose_name_plural = "GPIO Output Pins"
        
        
    name = models.CharField("Pin Name", max_length=50)
    # affects_variable = models.BooleanField(default=False)
    pin = models.SmallIntegerField("GPIO pin")
    device = models.ForeignKey(Device, verbose_name="Device", on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GPIOPin_detail", kwargs={"pk": self.pk})


class LocationData(models.Model):
    device = models.ForeignKey(Device, verbose_name=('Device'), on_delete=models.CASCADE)
    lat = models.FloatField("Latitude",default=0)
    lng = models.FloatField("Longtitude",default=0)
    date_time = models.DateTimeField("Date and time", null=True, default=timezone.now)
    
    
    
    
from django.utils import timezone
import secrets
import string


class ExpirableToken(models.Model):
    class Meta:
        db_table = 'expirable_token'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    expiration_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.token or self.is_expired:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(40))
    
    def set_expiration(self, days=0, hours=0, minutes=0):
        self.expiration_date = timezone.now() + timezone.timedelta(days=days, hours=hours, minutes=minutes)
        self.save()

    @property
    def is_expired(self):
        return self.expiration_date < timezone.now()
    
    
    