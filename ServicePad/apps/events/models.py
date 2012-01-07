from django.db import models
from ServicePad.apps.account.models import UserProfile

class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    public = models.BooleanField(default=True)
    category = models.ManyToManyField(EventCategory)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    list_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(UserProfile)
    rating = models.PositiveSmallIntegerField()
    