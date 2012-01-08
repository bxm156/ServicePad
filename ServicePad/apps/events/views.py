# Create your views here.
from django.shortcuts import render_to_response, RequestContext
from forms import CreateEventForm

def list_my_events(request):
    pass
    
def create(request):
    if(request.POST):
        new_data = request.POST.copy()
        new_event = CreateEventForm(new_data)
        if new_event.is_valid():
            new_event.save()
        else:
            #show errors
            pass
    event_form = CreateEventForm()
    return render_to_response('create_event.html',
                       {'form':event_form},
                       RequestContext(request))
    
    
