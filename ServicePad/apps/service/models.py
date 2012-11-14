from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.team.models import Team
from ServicePad.apps.events.models import Event

# Create your models here.

class ServiceRecord(models.Model):
    user = models.ForeignKey(User, related_name='volunteer', null = True, blank = True)
    team = models.ForeignKey(Team, related_name='team', null=True, blank=True)
    event = models.ForeignKey(Event, null=False,blank=False)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    hours = models.DecimalField(max_digits = 5, decimal_places=2)
    rating = models.PositiveIntegerField()
    review = models.TextField()
    attended = models.BooleanField()
    
class ServiceEnrollment(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team, null=True,blank=True)
    event = models.ForeignKey(Event)
    enrollment_time = models.DateTimeField()
    approved = models.BooleanField()