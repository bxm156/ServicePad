from django.db import models
from ServicePad.apps.account.models import Host

class Event(models.Model):
    CATEGORY = (
                (0,'Academic'),
                (1,'Food'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    list_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Host)
    rating = models.PositiveSmallIntegerField()
    
    
