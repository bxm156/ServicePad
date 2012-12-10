# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from ServicePad.apps.events.models import Event
from ServicePad.apps.account.models import UserProfile, Availability, HasSkill, HasInterest, PROFICIENCY
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as djangoLogout
from ServicePad.apps.account.forms import VolunteerProfileForm, OrganizationProfileForm, AvailabilityForm, AddSkillForm, AddInterestForm
from ServicePad.apps.team.models import Team, TeamMembership
from ServicePad.apps.bookmarks.models import Bookmark
from ServicePad.apps.service.models import ServiceEnrollment
from datetime import datetime
from django.db import IntegrityError
from random import choice

@login_required
def index(request):
    if request.user.get_profile().account_type == 1:
        return events_organization(request)
    
    #Get a list of upcoming events the user has enrolled in, and were approved by the organization
    """
    SELECT `service_serviceenrollment`.`start`, `service_serviceenrollment`.`end`, `service_serviceenrollment`.`event_id`,
    `events_event`.`name`, `events_event`.`short_description`, `team_team`.`name` FROM `service_serviceenrollment`
    INNER JOIN `events_event` ON (`service_serviceenrollment`.`event_id` = `events_event`.`id`)
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE (`service_serviceenrollment`.`user_id` = 1  AND `service_serviceenrollment`.`approved` = 1 
    AND `service_serviceenrollment`.`end` > 2012-12-10 02:07:38 ) ORDER BY `service_serviceenrollment`.`start` ASC
    """
    upcoming_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=True).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
    print upcoming_enrolled.query.__str__()
    
    context = {'upcoming_enrollments':upcoming_enrolled}
    
    #Get recommended events
    recommended_events = Event.get_recommend(request.user.id,1) #Uses stored procedure
    if recommended_events:
        try:
            event_id = choice(recommended_events)
            event = Event.objects.get(pk=event_id)
            context.update({'recommendation':event,'name':request.user.get_full_name()})
        except:
            pass
    return render(request,'account_index.djhtml',context)
    
    
@login_required
def teams(request):
    #Teams the user is a member in
    """
    SELECT `team_teammembership`.`id`, `team_teammembership`.`member_id`, `team_teammembership`.`team_id`,
    `team_teammembership`.`join_date`, `team_teammembership`.`invite`, `team_team`.`id`, `team_team`.`name`,
    `team_team`.`join_date`, `team_team`.`admin_id` FROM `team_teammembership`
    INNER JOIN `team_team` ON (`team_teammembership`.`team_id` = `team_team`.`id`)
    WHERE (`team_teammembership`.`member_id` = 1  AND `team_teammembership`.`invite` = False )
    """
    teams = TeamMembership.objects.filter(member=request.user,invite=False).select_related('team')
    print teams.query.__str__()
    
    #Invites are teams the user has been invited to
    """
    SELECT `team_teammembership`.`id`, `team_teammembership`.`member_id`, `team_teammembership`.`team_id`,
    `team_teammembership`.`join_date`, `team_teammembership`.`invite`, `team_team`.`id`, `team_team`.`name`,
    `team_team`.`join_date`, `team_team`.`admin_id` FROM `team_teammembership`
    INNER JOIN `team_team` ON (`team_teammembership`.`team_id` = `team_team`.`id`)
    WHERE (`team_teammembership`.`member_id` = 1  AND `team_teammembership`.`invite` = True )
    """
    invites = TeamMembership.objects.filter(member=request.user,invite=True).select_related('team')
    print invites.query.__str__()
    
    teams = [ m.team for m in teams ]
    invites = [m.team for m in invites ]
    
    
    #Teams the user is an admin
    """
    SELECT `team_team`.`id`, `team_team`.`name`, `team_team`.`join_date`, `team_team`.`admin_id`
    FROM `team_team` WHERE `team_team`.`admin_id` = 1 
    """
    admin_of_teams = Team.objects.filter(admin=request.user) or None
    print Team.objects.filter(admin=request.user).query.__str__()
    
    context = { 'teams' : teams,
               'invites': invites,
                'admin_of_teams' : admin_of_teams }
    return render(request,'account_teams.djhtml',context)

@login_required
def profile(request):
    context = {'name':request.user.get_full_name(),'id':request.user.id}
    profile = request.user.get_profile()
    if request.method == 'POST':
        if profile.account_type == UserProfile.ACCOUNT_VOLUNTEER:
            profile_form = VolunteerProfileForm(request.POST,instance=profile)
        if profile.account_type == UserProfile.ACCOUNT_ORGANIZATION:
            profile_form = OrganizationProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            context.update({'success':True})
    else:
        if profile.account_type == UserProfile.ACCOUNT_VOLUNTEER:
            profile_form = VolunteerProfileForm(instance=profile)
        if profile.account_type == UserProfile.ACCOUNT_ORGANIZATION:
            profile_form = OrganizationProfileForm(instance=profile)
    context.update({'profile_form':profile_form})
    return render(request, 'profile.djhtml', context)

@login_required    
def events(request):
    if request.user.get_profile().account_type == 1:
        return events_organization(request)
    
    #Get a list of upcoming events
    """
    SELECT `service_serviceenrollment`.`start`, `service_serviceenrollment`.`end`, `service_serviceenrollment`.`event_id`,
    `events_event`.`name`, `events_event`.`short_description`, `team_team`.`name` FROM `service_serviceenrollment`
    INNER JOIN `events_event` ON (`service_serviceenrollment`.`event_id` = `events_event`.`id`)
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE (`service_serviceenrollment`.`user_id` = 1  AND `service_serviceenrollment`.`approved` = 1
    AND `service_serviceenrollment`.`end` > 2012-12-10 02:17:59 ) ORDER BY `service_serviceenrollment`.`start` ASC
    """
    upcoming_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=True).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
    print upcoming_enrolled.query.__str__()
    
    #Get a list of past approved enrollments
    """
    SELECT `service_serviceenrollment`.`start`, `service_serviceenrollment`.`end`, `service_serviceenrollment`.`event_id`,
    `events_event`.`name`, `events_event`.`short_description`, `team_team`.`name`
    FROM `service_serviceenrollment` INNER JOIN `events_event` ON (`service_serviceenrollment`.`event_id` = `events_event`.`id`)
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE (`service_serviceenrollment`.`user_id` = 1  AND `service_serviceenrollment`.`end` <= 2012-12-10 02:17:59 
    AND `service_serviceenrollment`.`approved` = 1 ) ORDER BY `service_serviceenrollment`.`start` DESC
    """
    past_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__lte=datetime.now(),approved=True).order_by('-start').values('start','end','event','event__name','event__short_description','team__name')
    print past_enrolled.query.__str__()
    
    #Get a list of upcoming enrollments that are still awaiting moderation
    """
    SELECT `service_serviceenrollment`.`start`, `service_serviceenrollment`.`end`, `service_serviceenrollment`.`event_id`,
    `events_event`.`name`, `events_event`.`short_description`, `team_team`.`name` FROM `service_serviceenrollment`
    INNER JOIN `events_event` ON (`service_serviceenrollment`.`event_id` = `events_event`.`id`)
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE (`service_serviceenrollment`.`user_id` = 1  AND `service_serviceenrollment`.`approved` = 0 
    AND `service_serviceenrollment`.`end` > 2012-12-10 02:17:59 ) ORDER BY `service_serviceenrollment`.`start` ASC
    """
    upcoming_pending = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=False).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
    print upcoming_pending.query.__str__()
 
    #Get the user's bookmarks
    """
    SELECT `bookmarks_bookmark`.`id`, `bookmarks_bookmark`.`user_id`, `bookmarks_bookmark`.`event_id`
    FROM `bookmarks_bookmark` WHERE `bookmarks_bookmark`.`user_id` = 1 
    """
    bookmarks = Bookmark.objects.filter(user=request.user)
    print bookmarks.query.__str__()
    
    return render(request,'account_events.djhtml',
                               {'bookmarks':bookmarks,
                                'upcoming_enrollments':upcoming_enrolled,
                                'past_enrollments':past_enrolled,
                                'pending_enrollments':upcoming_pending})
    
def events_organization(request):
    #Get the Organization's Created Events
    """
    SELECT `events_event`.`name`, `events_event`.`id` FROM `events_event` WHERE `events_event`.`owner_id` = 6 
    """
    events = Event.objects.filter(owner__exact=request.user).values('name','id')
    print events.query.__str__()
    
    #Get the Organizations Bookmarks
    """
    SELECT `bookmarks_bookmark`.`id`, `bookmarks_bookmark`.`user_id`, `bookmarks_bookmark`.`event_id`
    FROM `bookmarks_bookmark` WHERE `bookmarks_bookmark`.`user_id` = 6 
    """
    bookmarks = Bookmark.objects.filter(user=request.user)
    print  bookmarks.query.__str__()
    
    return render(request,'account_events_organization.djhtml',
                           {'events':events, 'bookmarks':bookmarks})
    
@login_required
def availability(request):
    context = {}
    if request.method == 'POST':
        form = AvailabilityForm(request.POST.copy(),instance=Availability(user=request.user))
        if form.is_valid():
            try:
                form.save()
                context.update({'added':True})
                form = AvailabilityForm()
            except IntegrityError, e:
                context.update({'error':True,'error_message':e[0]})
        else:
            context.update({'error':True})        
    else:
        form = AvailabilityForm()
    
    #get users availability   
    """
    SELECT `account_availability`.`id`, `account_availability`.`user_id`, `account_availability`.`start`, `account_availability`.`end`
    FROM `account_availability` WHERE `account_availability`.`user_id` = 1 
    """
    my_avail = Availability.objects.filter(user=request.user)
    print my_avail.query.__str__()
    
    context.update({'availability': my_avail,'form': form})
    return render(request, 'account_availability.djhtml', context)

@login_required
def availability_remove(request,a_id):
    avail = get_object_or_404(Availability,pk=a_id,user=request.user)
    avail.delete()
    return redirect("/account/availability/")
    
@login_required
def skills(request):
    context = {}
    if request.method == 'POST':
        hs = HasSkill(user=request.user)
        form = AddSkillForm(request.POST.copy(),instance=hs)
        if form.is_valid():
            try:
                form.save()
                context.update({'added':True})
                form = AddSkillForm()
            except IntegrityError, e:
                context.update({'error':True,'error_message':e[0]})
    else:
        form = AddSkillForm()
        
    #Get the user's skills
    """
    SELECT `account_hasskill`.`id`, `account_hasskill`.`proficiency_level`, `account_skill`.`name`
    FROM `account_hasskill` INNER JOIN `account_skill` ON (`account_hasskill`.`skill_id` = `account_skill`.`id`)
    WHERE `account_hasskill`.`user_id` = 1  ORDER BY `account_skill`.`name` ASC
    """
    my_skills = HasSkill.objects.filter(user=request.user).values('id','proficiency_level','skill__name').order_by('skill__name')
    print my_skills.query.__str__()
    
    context.update({
               'skills':my_skills,
               'levels':PROFICIENCY, 
               'form':form
               })
    
    return render(request,'account_skills.djhtml',context)

@login_required
def skill_remove(request,s_id):
    skill = get_object_or_404(HasSkill,pk=s_id,user=request.user)
    skill.delete()
    return redirect("/account/skills")

@login_required
def interest(request):
    context = {}
    if request.method == 'POST':
        hs = HasInterest(user=request.user)
        form = AddInterestForm(request.POST.copy(),instance=hs)
        if form.is_valid():
            try:
                form.save()
                context.update({'added':True})
                form = AddInterestForm()
            except IntegrityError, e:
                context.update({'error':True,'error_message':e[0]})
    else:
        form = AddInterestForm()
    #Get the user's interests
    """
    SELECT `account_hasinterest`.`id`, `account_hasinterest`.`level`, `account_interest`.`name` FROM `account_hasinterest`
    INNER JOIN `account_interest` ON (`account_hasinterest`.`interest_id` = `account_interest`.`id`)
    WHERE `account_hasinterest`.`user_id` = 1  ORDER BY `account_interest`.`name` ASC
    """
    my_interests = HasInterest.objects.filter(user=request.user).values('id','level','interest__name').order_by('interest__name')
    print my_interests.query.__str__()
    context.update({
               'interests':my_interests,
               'levels':PROFICIENCY, 
               'form':form
               })
    
    return render(request,'account_interests.djhtml',context)

@login_required
def interest_remove(request,i_id):
    interest = get_object_or_404(HasInterest,pk=i_id,user=request.user)
    interest.delete()
    return redirect("/account/interests")
    
def logout(request):
    if request.user.is_authenticated():
        djangoLogout(request)
    return redirect("/")
    