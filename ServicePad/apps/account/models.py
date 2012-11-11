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
    ACCOUNT_ORGANIZATION = 1
    ACCOUNT_TYPE = (
                    (ACCOUNT_VOLUNTEER,'Volunteer'),
                    (ACCOUNT_ORGANIZATION,'Organization'),
                    )
    ETHNICITY_WHITE = 'w'
    ETHNICITY_OTHER = 'oth'
    ETHNICITY = (
			(ETHNICITY_WHITE, 'White'),
			(ETHNICITY_OTHER, 'Other'),
			)
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE, default=ACCOUNT_VOLUNTEER,editable=False)
    gender = models.CharField(max_length=2, choices=GENDER, default=GENDER_NOT_SPECIFIED)
    ethnicity = models.CharField(max_length=3, choices=ETHNICITY, default=ETHNICITY_WHITE)
    major = models.CharField(max_length=20, blank=True, null=True)
    graduating_class = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    postalzip = models.CharField(max_length=11)
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION, default=AUTH_MANUAL,editable=False)
    user = models.OneToOneField(User, primary_key=True, parent_link=True,editable=False)
    
    #Business Only fields
    organization_name = models.CharField(max_length=60, blank=True, null=True)
    organization_address = models.CharField(max_length=60, blank=True, null=True)
    organization_city = models.CharField(max_length=60, blank=True, null=True)
    organization_state = models.CharField(max_length=2, blank=True, null=True)
    organization_postalzip = models.CharField(max_length=11, blank=True, null=True)
    organization_phone = models.CharField(max_length=30, blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=30, blank=False)
    members = models.ManyToManyField(User, through='TeamMembership')
    join_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(UserProfile, related_name='admin')
    
class TeamMembership(models.Model):
    member = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    join_date = models.DateTimeField(auto_now_add=True)
    invite = models.BooleanField(default=True) # True if pending invite, user must accept to join
    
class Skill(models.Model):
    name = models.CharField(max_length=30)

class HasSkill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    proficiency_level = models.PositiveSmallIntegerField()

class Interest(models.Model):
    name = models.CharField(max_length=30)
    
class HasInterest(models.Model):
    user = models.ForeignKey(User)
    interest = models.ForeignKey(Interest)
    level = models.PositiveSmallIntegerField()

class Availability(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField()
    end = models.DateTimeField()
