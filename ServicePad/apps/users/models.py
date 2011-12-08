from django.db import models

class User(models.Model):
    GENDER = (
              ('m','Male'),
              ('f','Female'),
    )
    AUTHENTICATION = (
                      (1,'Manual'),
                      (2, 'CAS'),
    )
    first_name = models.CharField(max_length=30,blank=False)
    last_name = models.CharField(max_length=30,blank=False)
    email = models.EmailField(max_length=75,unique=True)
    password = models.CharField(max_length=32)
    gender = models.CharField(max_length=2, choices=GENDER)
    address = models.CharField(max_length=60,blank=True,null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    authentication = models.PositiveSmallIntegerField(choices=AUTHENTICATION)
    
    class Meta:
        abstract = True
        
    
class Volunteer(User):
    pass
      
class Host(User):
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