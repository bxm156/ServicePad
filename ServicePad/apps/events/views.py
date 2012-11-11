# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from forms import CreateEventForm
from django.contrib.auth.decorators import login_required
from models import Event

@login_required
def create(request):
    if request.POST:
        new_data = request.POST.copy()
        event_form = CreateEventForm(new_data)
        if event_form.is_valid():
            new_event = event_form.save(request.user)
            return redirect(new_event)
        else:
            return render(request,'create.djhtml',
                       {'form':event_form,
                        'errors':event_form.errors})
    event_form = CreateEventForm()
    return render(request,'create.djhtml',
                       {'form':event_form})
    
def view(request,id):
    event = get_object_or_404(Event, pk=id)
    return render(request,'view.djhtml',
                       {'event':event})
    
