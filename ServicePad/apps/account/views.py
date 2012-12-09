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
    if request.user.is_authenticated():
        upcoming_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=True).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
        context = {'upcoming_enrollments':upcoming_enrolled}
        #Get a list of stuff to show on the page
        
        #Get recommended events
        recommended_events = Event.get_recommend(request.user.id,1)
        if recommended_events:
            try:
                event_id = choice(recommended_events)
                event = Event.objects.get(pk=event_id)
                context.update({'recommendation':event,'name':request.user.get_full_name()})
            except:
                pass
        return render(request,'account_index.djhtml',context)
    return redirect("/")

@login_required
def teams(request):
    #Teams the user is a member in
    #Invites are teams the user has been invited to
    teams = TeamMembership.objects.filter(member=request.user,invite=False).select_related('team')
    invites = TeamMembership.objects.filter(member=request.user,invite=True).select_related('team')
    teams = [ m.team for m in teams ]
    invites = [m.team for m in invites ]
    
    
    #Teams the user is an admin
    admin_of_teams = Team.objects.filter(admin=request.user) or None
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
    print datetime.now()
    upcoming_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=True).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
    print upcoming_enrolled.query.__str__()
    past_enrolled = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__lte=datetime.now(),approved=True).order_by('-start').values('start','end','event','event__name','event__short_description','team__name')
    upcoming_pending = ServiceEnrollment.objects.select_related('event','team').filter(user=request.user,end__gt=datetime.now(),approved=False).order_by('start').values('start','end','event','event__name','event__short_description','team__name')
 
    events = Event.objects.filter(owner__exact=request.user)
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request,'account_events.djhtml',
                               {'events':events, 'bookmarks':bookmarks,
                                'upcoming_enrollments':upcoming_enrolled,
                                'past_enrollments':past_enrolled,
                                'pending_enrollments':upcoming_pending})
    
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
    my_avail = Availability.objects.filter(user=request.user)
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
    my_skills = HasSkill.objects.filter(user=request.user).values('id','proficiency_level','skill__name').order_by('skill__name')
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
    my_interests = HasInterest.objects.filter(user=request.user).values('id','level','interest__name').order_by('interest__name')
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
    