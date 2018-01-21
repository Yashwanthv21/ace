from django.db import models
from django.contrib.auth.models import User

class Data(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    imei = models.CharField(max_length=15)
    s_str = models.CharField(max_length=10, null=True, blank=True)
    dev_time = models.DateTimeField(null=True,blank=True)
    temperature = models.CharField(max_length=10, null=True, blank=True)
    humidity = models.CharField(max_length=10, null=True, blank=True)

class UsersImei(models.Model):
    imei_numbers = models.CharField(max_length=15)
    device_name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    class Meta:
        unique_together = ('imei_numbers','user',)