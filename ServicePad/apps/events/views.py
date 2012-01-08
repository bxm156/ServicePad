# Create your views here.
from django.shortcuts import render_to_response, RequestContext, redirect
from forms import CreateEventForm
from django.contrib.auth.decorators import login_required

def list_my_events(request):
    pass
    
@login_required
def create(request):
    if request.POST:
        new_data = request.POST.copy()
        event_form = CreateEventForm(new_data)
        if event_form.is_valid():
            new_event = event_form.save(request.user)
            return redirect(new_event)
        else:
            return render_to_response('create_event.html',
                       {'form':event_form,
                        'errors':event_form.errors},
                       RequestContext(request))
    event_form = CreateEventForm()
    return render_to_response('create_event.html',
                       {'form':event_form},
                       RequestContext(request))
    
def view(request,id):
    event_form = CreateEventForm()
    return render_to_response('create_event.html',
                       {'form':event_form},
                       RequestContext(request))
    
