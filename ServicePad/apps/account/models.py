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
    gender = models.CharField(max_length=2, choices=GENDER, default=GENDER_NOT_SPECIFIED, null=True)
    ethnicity = models.CharField(max_length=3, choices=ETHNICITY, default=ETHNICITY_WHITE, null=True)
    major = models.CharField(max_length=20, blank=True, null=True)
    graduating_class = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=60,verbose_name="Personal Address")
    city = models.CharField(max_length=60,verbose_name="Personal City")
    state = models.CharField(max_length=2,verbose_name="Personal State")
    postalzip = models.CharField(max_length=11,verbose_name="Personal Zip")
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION, default=AUTH_MANUAL,editable=False)
    user = models.OneToOneField(User, primary_key=True, parent_link=True,editable=False)
    
    #Business Only fields
    organization_name = models.CharField(max_length=60, blank=True, null=True)
    organization_address = models.CharField(max_length=60, blank=True, null=True)
    organization_city = models.CharField(max_length=60, blank=True, null=True)
    organization_state = models.CharField(max_length=2, blank=True, null=True)
    organization_postalzip = models.CharField(max_length=11, blank=True, null=True)
    organization_phone = models.CharField(max_length=30, blank=True, null=True)
    
class Skill(models.Model):
    name = models.CharField(max_length=30,unique=True)
    
    def __unicode__(self):
        return self.name

PROFICIENCY = (
              (0, 'Beginner'),
              (1, 'Advanced'),
              (2, 'Expert'),
)

class HasSkill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    proficiency_level = models.PositiveSmallIntegerField(choices=PROFICIENCY,default=0)
    
    class Meta:
        unique_together = (("user", "skill"))

class Interest(models.Model):
    name = models.CharField(max_length=30,unique=True)
    
    def __unicode__(self):
        return self.name
    
class HasInterest(models.Model):
    user = models.ForeignKey(User)
    interest = models.ForeignKey(Interest)
    level = models.PositiveSmallIntegerField(choices=PROFICIENCY,default=0)
    
    class Meta:
        unique_together = (("user", "interest"))

class Availability(models.Model):
    user = models.ForeignKey(User)
    start = models.TimeField(help_text="ex: 11:30")
    end = models.TimeField(help_text="ex: 13:30")
    
    class Meta:
        unique_together = (("user", "start", "end"))
