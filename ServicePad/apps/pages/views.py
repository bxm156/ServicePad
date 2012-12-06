# Create your views here.
from django.shortcuts import render, get_object_or_404
from ServicePad.apps.events.models import Event
from ServicePad.apps.team.models import Team, TeamMembership
from ServicePad.apps.service.models import ServiceEnrollment
from ServicePad.apps.account.models import UserProfile, Availability, HasSkill, HasInterest
from datetime import datetime
from django.db.models import Count
from django.db import connection
from django.contrib.auth.models import User

def index(request):
    #5 Upcoming events
    upcoming_events = Event.objects.filter(start_time__gt=datetime.now()).values('id','name').order_by('-start_time')[:5]
    
    #Top 5 teams with the most enrollments in service
    top_5_teams = ServiceEnrollment.objects.values('team__id').filter(team__isnull=False).annotate(count=Count('id')).order_by('-count').values('team__name','team__id','count')[:5]
    print top_5_teams.query.__str__()
    
    # Top 5 Users in Service
    top_5_users = ServiceEnrollment.objects.values('user').annotate(count=Count('id')).order_by('-count').values('user__id','user__first_name','user__last_name','count')[:5]
    print top_5_users.query.__str__()
    
    # Total Service Hours
    #This will only work on our MySQL instance, not local SQLite
    try:
        
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(`seconds`) AS total_seconds FROM  (SELECT TIMESTAMPDIFF(SECOND,`service_serviceenrollment`.`start`,`service_serviceenrollment`.`end`) AS seconds FROM `service_serviceenrollment`) AS TEMP")
        row = cursor.fetchone()
        cursor.close()
        seconds = row[0]
        if seconds == None:
            raise Exception
        hours = float(float(seconds)/(60.0*60.0))
    except:
        #Dummy value for SQLite users
        hours = 0
    
    
    show_account_link = False
    if request.user.is_authenticated():
        show_account_link = True
    context = {'user_loggedin': show_account_link, 'upcoming_events':upcoming_events,'hours':hours}
    return render(request,'index.djhtml',context)

def public_profile(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    profile = get_object_or_404(UserProfile,pk=user_id)
    availability = Availability.objects.filter(user=request.user)
    skills = HasSkill.objects.filter(user=request.user)
    interests = HasInterest.objects.filter(user=request.user)
    past_events = ServiceEnrollment.objects.filter(user=request.user,end__lte=datetime.now())
    teams = Team.objects.filter(members=request.user).values('id','name','teammembership__join_date')
    context = {
               'name':user.get_full_name(),
               'profile':profile,
               'availability':availability,
               'skills':skills,
               'interests':interests,
               'events':past_events,
               'teams':teams
               }
    return render(request,'public_profile.djhtml',context)
    
    
    