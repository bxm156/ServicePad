# Create your views here.
from django.shortcuts import render, get_object_or_404
from ServicePad.apps.events.models import Event
from ServicePad.apps.team.models import Team
from ServicePad.apps.service.models import ServiceRecord, ServiceEnrollment
from ServicePad.apps.account.models import UserProfile, Availability, HasSkill, HasInterest, PROFICIENCY
from datetime import datetime
from django.db.models import Count, Sum
from django.contrib.auth.models import User

def index(request):
    #5 Upcoming events
    """
    SELECT `events_event`.`id`, `events_event`.`name` FROM `events_event`
    WHERE `events_event`.`start_time` > 2012-12-10 01:24:56 
    ORDER BY `events_event`.`start_time` DESC LIMIT 5
    """
    upcoming_events = Event.objects.filter(start_time__gt=datetime.now()).values('id','name').order_by('-start_time')[:5]
    print upcoming_events.query.__str__()
    
    
    #Out of all events, order them randomly, narrow queryset to 1, and get that value from the queryset
    """
    SELECT `events_event`.`id`, `events_event`.`name`, `events_event`.`long_description`
    FROM `events_event` ORDER BY RAND() LIMIT 1
    """
    random_event = Event.objects.all().order_by('?').values('id','name','long_description')[:1][0]
    print Event.objects.all().order_by('?').values('id','name','long_description')[:1].query.__str__()
    
    #Top 5 teams with the most enrollments in service
    """
    SELECT `team_team`.`name`, `service_serviceenrollment`.`team_id`, COUNT(`service_serviceenrollment`.`id`) AS `count`
    FROM `service_serviceenrollment`
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE `team_team`.`id` IS NOT NULL
    GROUP BY `service_serviceenrollment`.`team_id`, `team_team`.`name`
    ORDER BY `count` DESC LIMIT 5

    """
    top_5_teams = ServiceEnrollment.objects.values('team__id').filter(team__isnull=False).annotate(count=Count('id')).order_by('-count').values('team__name','team__id','count')[:5]
    print top_5_teams.query.__str__()
    
    # Top 5 Users in Service
    """
    SELECT `service_serviceenrollment`.`user_id`, `auth_user`.`first_name`, `auth_user`.`last_name`,
    COUNT(`service_serviceenrollment`.`id`) AS `count` FROM `service_serviceenrollment`
    INNER JOIN `auth_user` ON (`service_serviceenrollment`.`user_id` = `auth_user`.`id`)
    GROUP BY `service_serviceenrollment`.`user_id`, `auth_user`.`first_name`, `auth_user`.`last_name`
    ORDER BY `count` DESC LIMIT 5
    """
    top_5_users = ServiceEnrollment.objects.values('user').annotate(count=Count('id')).order_by('-count').values('user__id','user__first_name','user__last_name','count')[:5]
    print top_5_users.query.__str__()
    
    #Total Service hours performed
    """
    SELECT SUM(`service_servicerecord`.`hours`) AS `hours`
    FROM `service_servicerecord`
    WHERE `service_servicerecord`.`attended` = 1
    """
    total_hours = ServiceRecord.objects.filter(attended=True).aggregate(hours=Sum('hours'))
    
    
    show_account_link = False
    if request.user.is_authenticated():
        show_account_link = True
    context = {'user_loggedin': show_account_link, 'upcoming_events':upcoming_events, 'random': random_event, 'upcoming': upcoming_events}
    context.update(total_hours)
    return render(request,'index.djhtml',context)

def public_profile(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    profile = get_object_or_404(UserProfile,pk=user_id)
    if profile.account_type == 0:
        return volunteer_profile(request,user_id,user,profile)
    if profile.account_type == 1:
        return organization_profile(request,user_id,user,profile)

def volunteer_profile(request,user_id,user,profile):
    availability = Availability.objects.filter(user=user_id)
    skills = HasSkill.objects.filter(user=user_id).values('skill__name')
    interests = HasInterest.objects.filter(user=user_id).values('interest__name','level')
    past_events = ServiceRecord.objects.filter(user=user_id,end__lte=datetime.now()).values('event_id','event__name','hours','review')
    review = ServiceRecord.objects.filter(user=user_id).extra(where=['LENGTH(review) >= 5']).values('event__owner','review','rating','event__owner__userprofile__organization_name').order_by('?')[:1]
    total_hours = ServiceRecord.objects.filter(user=user_id).aggregate(total_hours=Sum('hours'))
    print total_hours
    if review:
        review = review[0]
    teams = Team.objects.filter(members=user_id).values('id','name','teammembership__join_date')
    print review
    context = {
               'user':user,
               'profile':profile,
               'availability':availability,
               'skills':skills,
               'interests':interests,
               'events':past_events,
               'teams':teams,
               'levels':PROFICIENCY,
               'review':review
               }
    context.update(total_hours)
    return render(request,'public_profile_volunteer.djhtml',context)

def organization_profile(request,user_id,user,profile):
    upcoming_events = Event.objects.filter(owner=user_id,start_time__gt=datetime.now()).values('id','name','start_time','end_time')
    current_events = Event.objects.filter(owner=user_id,start_time__lte=datetime.now(),end_time__gt=datetime.now()).values('id','name','start_time','end_time')
    past_events = Event.objects.filter(owner=user_id,end_time__lte=datetime.now()).values('id','name','start_time','end_time')
    print upcoming_events
    print current_events
    print past_events
    context = {'profile':profile,'user':user,'upcoming_events':upcoming_events,'current_events':current_events,'past_events':past_events}
    return render(request,'public_profile_organization.djhtml',context)
    
    
