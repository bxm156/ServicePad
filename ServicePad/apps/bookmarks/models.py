from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.events.models import Event

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

