# Create your views here.
from django.shortcuts import render_to_response, redirect, RequestContext
from ServicePad.apps.events.models import Event
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_authenticated():
        return render_to_response('account_index.html',{},
                                  context_instance=RequestContext(request))
    return redirect("/")


def teams(request):
    pass

def profile(request):
    pass

def track(request):
    pass

@login_required    
def events(request):
    events = Event.objects.filter(owner__exact=request.user)
    return render_to_response('account_events.html',
                               {'events':events},
                               RequestContext(request))