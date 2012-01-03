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
    ACCOUNT_VOLUNTEER = 0
    ACCOUNT_HOST = 1
    ACCOUNT_TYPE = (
                    (ACCOUNT_VOLUNTEER,'Volunteer'),
                    (ACCOUNT_HOST,'Host'),
                    )
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE, default=ACCOUNT_VOLUNTEER)
    gender = models.CharField(max_length=2, choices=GENDER, default=GENDER_NOT_SPECIFIED)
    address = models.CharField(max_length=60, blank=True, null=True)
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION, default=AUTH_MANUAL)
    activation_key = models.CharField(max_length=32)
    key_expires = models.DateTimeField()
    user = models.OneToOneField(User, primary_key=True, parent_link=True)
    business_name = models.CharField(max_length=60, blank=True, null=True)
    business_address = models.CharField(max_length=60, blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=30, blank=False)
    members = models.ManyToManyField(UserProfile, through='TeamMembership')
    join_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(UserProfile, related_name='admin')
    
class TeamMembership(models.Model):
    member = models.ForeignKey(UserProfile)
    group = models.ForeignKey(Team)
    join_date = models.DateTimeField(auto_now_add=True)
    invite = models.BooleanField(default=True) # True if pending invite, user must accept to join
    

    
