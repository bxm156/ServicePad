from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER = (
              ('m','Male'),
              ('f','Female'),
    )
    AUTHENTICATION = (
                      (1,'Manual'),
                      (2, 'CAS'),
    )
    gender = models.CharField(max_length=2, choices=GENDER)
    address = models.CharField(max_length=60,blank=True,null=True)
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION)
    user = models.ForeignKey(User, unique=True)
    class Meta:
        abstract = True
        
    
class Volunteer(UserProfile):
    pass
      
class Host(UserProfile):
    business_name = models.CharField(max_length=60,blank=False)
    business_address = models.CharField(max_length=60,blank=True,null=True)

class Team(models.Model):
    name = models.CharField(max_length=30,blank=False)
    members = models.ManyToManyField(Volunteer, through = 'TeamMembership')
    join_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Volunteer, related_name='admin')
    
class TeamMembership(models.Model):
    member = models.ForeignKey(Volunteer)
    group = models.ForeignKey(Team)
    join_date = models.DateTimeField(auto_now_add=True)
    invite = models.BooleanField(default=True) # True if pending invite, user must accept to join
    

    