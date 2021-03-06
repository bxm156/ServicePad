from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.team.models import Team
from ServicePad.apps.events.models import Event

RATING = (
              (1, 'Terrible'),
              (2, 'Bad'),
              (3, 'Neutral'),
              (4, 'Good'),
              (5, 'Excellent'),
)

class ServiceRecord(models.Model):
    user = models.ForeignKey(User, related_name='volunteer', null=False, blank=False)
    team = models.ForeignKey(Team, related_name='team', null=True, blank=True)
    event = models.ForeignKey(Event, null=False,blank=False)
    start = models.DateTimeField(help_text="ex: YYYY-MM-DD HH:MM:SS")
    end = models.DateTimeField(help_text="ex: YYYY-MM-DD HH:MM:SS")
    hours = models.DecimalField(max_digits = 5, decimal_places=2,null=True)
    rating = models.PositiveIntegerField(choices=RATING,default=3)
    review = models.TextField()
    attended = models.BooleanField()
    
    class Meta:
        unique_together = (("user", "event", "start", "end"))
    
class ServiceEnrollment(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team, null=True,blank=True)
    event = models.ForeignKey(Event)
    start = models.DateTimeField(null=False,blank=False,help_text="ex: YYYY-MM-DD HH:MM:SS")
    end = models.DateTimeField(null=False,blank=False,help_text="ex: YYYY-MM-DD HH:MM:SS")
    enrollment_time = models.DateTimeField(auto_now=True)
    approved = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = (("user", "event", "start", "end"))