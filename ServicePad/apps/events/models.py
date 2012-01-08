from django.db import models
from ServicePad.apps.account.models import UserProfile

CATEGORY_NONE = 0
CATEGORY_INDOOR = 1
CATEGORY_OUTDOOR = 2
CATEGORY_FOOD = 3
CATEGORY_ANIMAL = 4

CATEGORY_CHOICES = (
                    (CATEGORY_NONE,"None"),
                    (CATEGORY_INDOOR,"Indoor"),
                    (CATEGORY_OUTDOOR,"Outdoor"),
                    (CATEGORY_FOOD,"Food"),
                    (CATEGORY_ANIMAL,"Animal"),
                    )


class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    public = models.BooleanField(default=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    list_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(UserProfile)
    #rating = models.PositiveSmallIntegerField()
    
    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.events.views.view', [str(self.id)])
    