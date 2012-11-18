from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.events.models import Event

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.events.views.view', [str(self.event.id)])
