# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from forms import CreateEventForm
from django.contrib.auth.decorators import login_required
from models import Event
from models import EventCategory
from ServicePad.apps.service.forms import ServiceEnrollmentForm, TeamForm
from ServicePad.apps.service.models import ServiceEnrollment, ServiceRecord
from ServicePad.apps.team.models import Team
from django.db.models import Count, Sum

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

@login_required 
def join(request,event_id,team_id=None,*args,**kwargs):
    show_teams = kwargs.get('show_teams')
    event = get_object_or_404(Event,pk=event_id)
    user = request.user
    is_team_admin = False
    context = {'tid' : team_id or 0}
    #Check is a team admin
    if show_teams is None:
        team_admin = Team.objects.filter(admin=user).values('id')
        is_team_admin = (len(team_admin) != 0)
        members = None
    else:
        team_admin = Team.objects.filter(admin=user).values('id','name')
        context.update({'team_select':team_admin})
        if team_id is None:
            team_id = team_admin[0]['id']
            team_name = team_admin[0]['name']
        if team_id is not None:
            team = get_object_or_404(Team,pk=team_id,admin=request.user)
            context.update({'tid':team_id})
            context.update({'tname':team.name})
            members = team.members.all().values('id','first_name','last_name')
            members = [(i['id'], "{} {}".format(i['first_name'],i['last_name'])) for i in members]
    
    if request.method == "POST":
        se = ServiceEnrollment(user=user,event=event)
        form = ServiceEnrollmentForm(request.POST.copy(),instance=se,prefix="time")
        team_form = TeamForm(request.POST.copy(),members=members,prefix="team")
        
        # Single User
        if team_id is None and form.is_valid():
            form.save()
            return redirect("/account/events/")
        
        #Team
        if team_id and form.is_valid() and team_form.is_valid():
            for (member_id) in team_form.get_selected_members():
                se = ServiceEnrollment(user_id=member_id,event=event,team=team)
                member_form = ServiceEnrollmentForm(request.POST.copy(),instance=se,prefix="time")
                if member_form.is_valid():
                    member_form.save()
            return redirect(team)
    else:
        form = ServiceEnrollmentForm(prefix="time")
        team_form = None
        if team_id:
            team_form = TeamForm(prefix="team",members=members)
    context.update({'tid':int(context['tid'])})
    context.update({'event':event, 'user':user, 'form':form, 'team_form':team_form, 'is_team_admin':is_team_admin})
    return render(request,'join_event.djhtml',context)

    
def view(request,id):
    event = get_object_or_404(Event.objects.select_related('category'), pk=id)
    #top_users = ServiceEnrollment.objects.values('user').filter(event=event).values('user_id','user__first_name','user__last_name').annotate(count=Count('id')).order_by('-count')[:5]
    top_users = ServiceRecord.objects.values('user').filter(event=event,attended=True).values('user_id','user__first_name','user__last_name',).annotate(hours=Sum('hours')).order_by('-hours')[:5]
    total_hours = ServiceRecord.objects.filter(event=event,attended=True).aggregate(Sum('hours'))
    context = {'event':event,'top_users':top_users}
    context.update(total_hours)
    print top_users.query.__str__()
    return render(request,'view_event.djhtml',context)

def list(request):
    event_cat = EventCategory.objects.all()
    if request.POST:
        data = request.POST.copy()
        category = int(data['category'])
        print category
        if category > 0:
            events = Event.objects.filter(category_id=category)
        else:
            events = Event.objects.all()
        return render(request, 'list_events.djhtml',
                        {'events': events,
                        'event_cat': event_cat})
    #this will only run if the if statement was not tripped
    events = Event.objects.all()
    return render(request, 'list_events.djhtml',
                    {'events': events,
                    'event_cat': event_cat})
