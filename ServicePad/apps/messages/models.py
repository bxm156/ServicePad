from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    toUser = models.ForeignKey(User,related_name="toUser")
    fromUser = models.ForeignKey(User,related_name="fromUser")
    subject = models.CharField(max_length=30,blank=True,null=True)
    message = models.TextField(max_length=500)
    date_sent = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.messages.views.message', [str(self.id)])