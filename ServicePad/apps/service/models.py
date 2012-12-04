from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.team.models import Team
from ServicePad.apps.events.models import Event

class ServiceRecord(models.Model):
    user = models.ForeignKey(User, related_name='volunteer', null = True, blank = True)
    team = models.ForeignKey(Team, related_name='team', null=True, blank=True)
    event = models.ForeignKey(Event, null=False,blank=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    hours = models.DecimalField(max_digits = 5, decimal_places=2)
    rating = models.PositiveIntegerField()
    review = models.TextField()
    attended = models.BooleanField()
    
    class Meta:
        unique_together = (("user", "event", "start", "end"))
    
class ServiceEnrollment(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team, null=True,blank=True)
    event = models.ForeignKey(Event)
    start = models.DateTimeField(null=False,blank=False)
    end = models.DateTimeField(null=False,blank=False)
    enrollment_time = models.DateTimeField(auto_now=True)
    approved = models.BooleanField()
    
    class Meta:
        unique_together = (("user", "event", "start", "end"))