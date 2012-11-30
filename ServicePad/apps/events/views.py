# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from forms import CreateEventForm
from django.contrib.auth.decorators import login_required
from models import Event
from models import EventCategory

@login_required
def create(request):
    if request.POST:
        new_data = request.POST.copy()
        event_form = CreateEventForm(new_data)
        if event_form.is_valid():
            #Create the event and save the values to it
            event = Event(owner=request.user)
            new_event_form = CreateEventForm(new_data,instance=event)
            new_event = new_event_form.save()
            return redirect(new_event)
        else:
            return render(request,'create_event.djhtml',
                       {'form':event_form,
                        'errors':event_form.errors})
    event_form = CreateEventForm()
    return render(request,'create_event.djhtml',
                       {'form':event_form})
    
def view(request,id):
    event = get_object_or_404(Event, pk=id)
    return render(request,'view_event.djhtml',
                       {'event':event})

def list(request):
    if request.POST:
        data = request.POST.copy()
        category = int(data['category'])
        if category > 0:
            events = Event.objects.filter(category__exact = category)
        else:
            print 'test?'
            events = Event.objects.all()
        return render(request, 'list_events.djhtml',
                        {'events': events})
    #this will only run if the if statement was not tripped
    events = Event.objects.all()
    event_cat = EventCategory.objects.all()
    return render(request, 'list_events.djhtml',
                    {'events': events,
                    'event_cat': event_cat})
