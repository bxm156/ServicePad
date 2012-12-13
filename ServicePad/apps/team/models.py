from django.db import models
from django.contrib.auth.models import User
from ServicePad.apps.events.models import Event

class Team(models.Model):
    name = models.CharField(max_length=30, blank=False)
    members = models.ManyToManyField(User, through='TeamMembership')
    join_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, related_name='admin')
    
    @models.permalink
    def get_absolute_url(self):
        return ('ServicePad.apps.team.views.view', [str(self.id)])
    
    @models.permalink
    def get_admin_url(self):
        return ('ServicePad.apps.team.views.admin', [str(self.id)])
    
    @models.permalink
    def get_accept_url(self):
        return ('ServicePad.apps.team.views.accept', [str(self.id)])
    
    @models.permalink
    def get_decline_url(self):
        return ('ServicePad.apps.team.views.decline', [str(self.id)])
    
class TeamMembership(models.Model):
    member = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    join_date = models.DateTimeField(auto_now_add=True)
    invite = models.BooleanField(default=True) # True if pending invite, user must accept to join
    
    class Meta:
        unique_together = (("member", "team"))