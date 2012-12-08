from django.db import models, connection
from django.contrib.auth.models import User
from ServicePad.apps.account.models import Skill


CATEGORY_NONE = 0
CATEGORY_INDOOR = 1
CATEGORY_OUTDOOR = 2
CATEGORY_FOOD = 3
CATEGORY_ANIMAL = 4

CATEGORY_CHOICES = (
                    (CATEGORY_INDOOR,"Indoor"),
                    (CATEGORY_OUTDOOR,"Outdoor"),
                    (CATEGORY_FOOD,"Food"),
                    (CATEGORY_ANIMAL,"Animal"),
                    )


class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    postalzip = models.CharField(max_length=11)
    public = models.BooleanField(default=True)
    category = models.ForeignKey(EventCategory)
    start_time = models.DateTimeField(help_text="ex: YYYY-MM-DD HH:MM:SS")
    end_time = models.DateTimeField(help_text="ex: YYYY-MM-DD HH:MM:SS")
    list_date = models.DateTimeField(auto_now_add=True,editable=False)
    owner = models.ForeignKey(User,editable=False)
    #rating = models.PositiveSmallIntegerField()
    #TODO: Support event pictures
    
    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.events.views.view', [str(self.id)])
    
    @staticmethod
    def get_recommend(user_id,threshold=1):
        """
        Returns a list of recommended events based on users enrollment
        """
        #Get recommendations based on Stored Procedure
        #Market Basket Problem in class
        try:
            cursor = connection.cursor()
            cursor.callproc("recommend_events", (user_id, threshold))# calls PROCEDURE named recommend_events
            results = cursor.fetchall()
            cursor.close()
            return [ int(i[0]) for i in results ]
        except:
            return None
    
class NeedsSkill(models.Model):
    event = models.ForeignKey(Event)
    skill = models.ForeignKey(Skill)
    min_proficiency_level = models.PositiveSmallIntegerField()
