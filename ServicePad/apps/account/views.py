# Create your views here.
from django.shortcuts import render_to_response, redirect, RequestContext, render
from ServicePad.apps.events.models import Event
from ServicePad.apps.account.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as djangoLogout
from ServicePad.apps.account.forms import VolunteerProfileForm, OrganizationProfileForm

@login_required
def index(request):
    if request.user.is_authenticated():
        return render_to_response('account_index.html',{},
                                  context_instance=RequestContext(request))
    return redirect("/")


def teams(request):
    pass

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

def track(request):
    pass

@login_required    
def events(request):
    events = Event.objects.filter(owner__exact=request.user)
    return render_to_response('account_events.html',
                               {'events':events},
                               RequestContext(request))
    
def logout(request):
    if request.user.is_authenticated():
        djangoLogout(request)
    return redirect("/")
    