# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from ServicePad.apps.events.models import Event
from ServicePad.apps.account.models import UserProfile, Availability
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as djangoLogout
from ServicePad.apps.account.forms import VolunteerProfileForm, OrganizationProfileForm, AvailabilityForm
from ServicePad.apps.team.models import Team, TeamMembership
from ServicePad.apps.bookmarks.models import Bookmark
from ServicePad.apps.service.models import ServiceEnrollment
from datetime import datetime

@login_required
def index(request):
    if request.user.is_authenticated():
        
        #Get a list of stuff to show on the page
        return render(request,'account_index.djhtml')
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
    profile = request.user.get_profile()
    if request.method == 'POST':
        if profile.account_type == UserProfile.ACCOUNT_VOLUNTEER:
            profile_form = VolunteerProfileForm(request.POST,instance=profile)
        if profile.account_type == UserProfile.ACCOUNT_ORGANIZATION:
            profile_form = OrganizationProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return render(request,'profile.djhtml', {'profile_form':profile_form})
    else:
        if profile.account_type == UserProfile.ACCOUNT_VOLUNTEER:
            profile_form = VolunteerProfileForm(instance=profile)
        if profile.account_type == UserProfile.ACCOUNT_ORGANIZATION:
            profile_form = OrganizationProfileForm(instance=profile)
        return render(request, 'profile.djhtml', {'profile_form':profile_form})

@login_required    
def events(request):
    print datetime.now()
    upcoming_enrolled = ServiceEnrollment.objects.select_related('event').filter(user=request.user,end__gt=datetime.now()).order_by('start').values('start','end','event','event__name','event__short_description')
    print upcoming_enrolled.query.__str__()
    past_enrolled = ServiceEnrollment.objects.select_related('event').filter(user=request.user,end__lte=datetime.now()).order_by('-start').values('start','end','event','event__name','event__short_description')
    events = Event.objects.filter(owner__exact=request.user)
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request,'account_events.djhtml',
                               {'events':events, 'bookmarks':bookmarks,
                                'upcoming_enrollments':upcoming_enrolled,
                                'past_enrollments':past_enrolled})
    
@login_required
def availability(request):
    context = {}
    if request.method == 'POST':
        form = AvailabilityForm(request.POST.copy(),instance=Availability(user=request.user))
        if form.is_valid():
            form.save()
            context.update({'added':True})
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
    return availability(request)
    
def logout(request):
    if request.user.is_authenticated():
        djangoLogout(request)
    return redirect("/")
    