from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_NOT_SPECIFIED = 'na'
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER = (
              (GENDER_NOT_SPECIFIED, 'Not Specified'),
              (GENDER_MALE, 'Male'),
              (GENDER_FEMALE, 'Female'),
    )
    AUTH_MANUAL = 1
    AUTH_CAS = 2 
    AUTHENTICATION = (
                      (AUTH_MANUAL, 'Manual'),
                      (AUTH_CAS, 'CAS'),
    )
    gender = models.CharField(max_length=2, choices=GENDER, default=GENDER_NOT_SPECIFIED)
    address = models.CharField(max_length=60, blank=True, null=True)
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION, default=AUTH_MANUAL)
    activation_key = models.CharField(max_length=32)
    key_expires = models.DateTimeField()
    user = models.OneToOneField(User)
    class Meta:
        abstract = True
        
    
class Volunteer(UserProfile):
    pass
      
class Host(UserProfile):
    business_name = models.CharField(max_length=60, blank=False)
    business_address = models.CharField(max_length=60, blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=30, blank=False)
    members = models.ManyToManyField(Volunteer, through='TeamMembership')
    join_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Volunteer, related_name='admin')
    
class TeamMembership(models.Model):
    member = models.ForeignKey(Volunteer)
    group = models.ForeignKey(Team)
    join_date = models.DateTimeField(auto_now_add=True)
    invite = models.BooleanField(default=True) # True if pending invite, user must accept to join
    

    
