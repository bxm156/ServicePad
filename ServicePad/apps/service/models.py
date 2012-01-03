from django.db import models
from ServicePad.apps.account.models import UserProfile
# Create your models here.

class ServiceRecord(models.Model):
    user = models.ForeignKey(UserProfile, related_name='volunteer')
    host = models.ForeignKey(UserProfile, related_name='host')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    hours = models.DecimalField(max_digits = 5, decimal_places=2)

    