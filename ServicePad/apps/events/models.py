from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.account.models import Skill

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
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    postalzip = models.CharField(max_length=11)
    public = models.BooleanField(default=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    list_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    #rating = models.PositiveSmallIntegerField()
    #TODO: Support event pictures
    
    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.events.views.view', [str(self.id)])
    
class NeedsSkill(models.Model):
    event = models.ForeignKey(Event)
    skill = models.ForeignKey(Skill)
    min_proficiency_level = models.PositiveSmallIntegerField()
