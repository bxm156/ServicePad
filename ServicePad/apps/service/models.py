from django.db import models
from ServicePad.apps.users.models import Volunteer, Host
# Create your models here.

class ServiceRecord(models.Model):
    user = models.ForeignKey(Volunteer)
    host = models.ForeignKey(Host)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    hours = models.DecimalField(max_digits = 5, decimal_places=2)

    