# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from ServicePad.apps.events.forms import CreateEventForm, NeedsSkillForm, SearchEventsForm
from django.contrib.auth.decorators import login_required
from ServicePad.apps.events.models import Event, NeedsSkill, EventCategory
from ServicePad.apps.service.forms import ServiceEnrollmentForm, TeamForm
from ServicePad.apps.service.models import ServiceEnrollment, ServiceRecord
from ServicePad.apps.team.models import Team
from django.db.models import Sum
from ServicePad.apps.events.decorators import event_admin
from datetime import datetime
from ServicePad.apps.account.models import PROFICIENCY
from django.db import connection
@login_required
def create(request):
    """
    Create a event
    """
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
    """
    Whean a team wants to join an event
    """
    show_teams = kwargs.get('show_teams')
    event = get_object_or_404(Event,pk=event_id)
    user = request.user
    is_team_admin = False
    context = {'tid' : team_id or 0}
    #Check is a team admin
    if show_teams is None:
        #Get the Team ids that this user administers
        """
        SELECT `team_team`.`id` FROM `team_team` WHERE `team_team`.`admin_id` = 1 
        """
        team_admin = Team.objects.filter(admin=user).values('id')
        print team_admin.query.__str__()
        
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
            
            #Get the names and ids of all the members
            """
            SELECT `auth_user`.`id`, `auth_user`.`first_name`, `auth_user`.`last_name` FROM `auth_user`
            INNER JOIN `team_teammembership` ON (`auth_user`.`id` = `team_teammembership`.`member_id`)
            WHERE `team_teammembership`.`team_id` = 1 
            """
            members = team.members.all().values('id','first_name','last_name')
            print members.query.__str__()
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
        # Insert an enrollment for each team member
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
    """
    View an event
    """
    if request.user.is_authenticated() and request.user.get_profile().account_type == 1:
        can_enroll = False
    else:
        can_enroll = True
        
    #Get the event
    """
    SELECT `events_event`.`id`, `events_event`.`name`, `events_event`.`short_description`, `events_event`.`long_description`,
    `events_event`.`address`, `events_event`.`city`, `events_event`.`state`, `events_event`.`postalzip`, `events_event`.`public`,
    `events_event`.`category_id`, `events_event`.`start_time`, `events_event`.`end_time`, `events_event`.`list_date`,
    `events_event`.`owner_id`, `events_eventcategory`.`id`, `events_eventcategory`.`name` FROM `events_event`
    INNER JOIN `events_eventcategory` ON (`events_event`.`category_id` = `events_eventcategory`.`id`)
    """
    event = get_object_or_404(Event.objects.select_related('category'), pk=id)
    print Event.objects.select_related('category').query.__str__()
    is_admin = (event.owner_id == request.user.id)
    
    #Get the top 5 users
    """
    SELECT `service_servicerecord`.`user_id`, `auth_user`.`first_name`, `auth_user`.`last_name`,
    SUM(`service_servicerecord`.`hours`) AS `hours` FROM `service_servicerecord`
    INNER JOIN `auth_user` ON (`service_servicerecord`.`user_id` = `auth_user`.`id`)
    WHERE (`service_servicerecord`.`attended` = True  AND `service_servicerecord`.`event_id` = 7 )
    GROUP BY `service_servicerecord`.`user_id`, `auth_user`.`first_name`, `auth_user`.`last_name`
    ORDER BY `hours` DESC LIMIT 5
    """
    top_users = ServiceRecord.objects.values('user').filter(event=event,attended=True).values('user_id','user__first_name','user__last_name',).annotate(hours=Sum('hours')).order_by('-hours')[:5]
    print top_users.query.__str__()
    
    #Get the total hours of service for this event
    """
    SELECT SUM(`service_servicerecord`.`hours`) AS `hours__sum` FROM `service_servicerecord`
    WHERE (`service_servicerecord`.`attended` = 1  AND `service_servicerecord`.`event_id` = 7
    """
    total_hours = ServiceRecord.objects.filter(event=event,attended=True).aggregate(Sum('hours'))
    print connection.queries
    
    #Get the needed skills
    """
    SELECT `events_needsskill`.`id`, `events_needsskill`.`event_id`, `events_needsskill`.`skill_id`,
    `events_needsskill`.`min_proficiency_level` FROM `events_needsskill`
    WHERE `events_needsskill`.`event_id` = 7 
    """
    needed_skills = NeedsSkill.objects.filter(event=event)
    print needed_skills.query.__str__()
    
    context = {'event':event,'top_users':top_users,'is_admin':is_admin,'needed_skills':needed_skills,'proficiency':PROFICIENCY,'can_enroll':can_enroll}
    context.update(total_hours)

    return render(request,'view_event.djhtml',context)

def list(request):
    event_cat = EventCategory.objects.all()
    form = SearchEventsForm()
    if request.POST:
        data = request.POST.copy()
        if data.get('show_all'):
            events = Event.objects.all()
        else:
            #Build the Query
            no_search = True
            events = Event.objects
            category = data['category']
            start = data['start']
            end = data['end']
            name = data['name']
            skill = data['skill']
            #check to see if an event has the name used
            if name != '':
                no_search = False
                events = events.filter(name__icontains=name) 
            #if the user searched by category
            if category != '':
                no_search = False
                events = events.filter(category_id=int(category))
            #if the user searched by time
            if start != '' and end != '':
                no_search = False
                events = events.filter(start_time__gt=start, end_time__lt=end)
            if skill != '':
                no_search = False
                events = events.select_related('needsskill').filter(skills = skill)
            if no_search:
                events = events.all()
        events = events.values('id', 'name', 'short_description').order_by('name')
        return render(request, 'list_events.djhtml',
                        {'events': events,
                        'form': form,
                        'event_cat': event_cat})
         
    #this will only run if the if statement was not tripped
    """
    SELECT `events_event`.`id`, `events_event`.`name`, `events_event`.`short_description`
    FROM `events_event` ORDER BY `events_event`.`name` ASC
    """
    events = Event.objects.all().values('id', 'name', 'short_description').order_by('name')
    print events.query.__str__()

    return render(request, 'list_events.djhtml',
                    {'events': events,
                    'form': form,
                    'event_cat': event_cat})

@event_admin
def admin(request,event_id):
    event = get_object_or_404(Event,pk=event_id)
    
    #Get ServiceEnrollments that have not yet been approved
    """
   SELECT `service_serviceenrollment`.`id`, `service_serviceenrollment`.`event_id`, `auth_user`.`first_name`,
   `auth_user`.`first_name`, `auth_user`.`last_name`, `service_serviceenrollment`.`user_id`,
   `service_serviceenrollment`.`team_id`, `team_team`.`name`, `service_serviceenrollment`.`start`,
   `service_serviceenrollment`.`end` FROM `service_serviceenrollment`
   INNER JOIN `auth_user` ON (`service_serviceenrollment`.`user_id` = `auth_user`.`id`)
   LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
   WHERE (`service_serviceenrollment`.`start` > 2012-12-10 05:33:15  AND `service_serviceenrollment`.`event_id` = 1  
   AND `service_serviceenrollment`.`approved` = 0 )
    """
    pending_approval = ServiceEnrollment.objects.filter(event=event,start__gt=datetime.now(),approved=0).values('id','event_id','user__first_name',
                    'user__first_name','user__last_name','user_id','team_id','team__name','start','end')
    print pending_approval.query.__str__()
    
    #Get approved ServiceEnrollments that are not in the past
    """
    SELECT `events_event`.`owner_id`, T4.`first_name`, T4.`last_name`, `service_serviceenrollment`.`team_id`,
    `team_team`.`name`, `service_serviceenrollment`.`start`, `service_serviceenrollment`.`end`
    FROM `service_serviceenrollment` INNER JOIN `events_event` ON (`service_serviceenrollment`.`event_id` = `events_event`.`id`)
    INNER JOIN `auth_user` T4 ON (`service_serviceenrollment`.`user_id` = T4.`id`)
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`)
    WHERE (`service_serviceenrollment`.`end` > 2012-12-10 05:33:15  AND `service_serviceenrollment`.`event_id` = 1 
    AND `service_serviceenrollment`.`approved` = 1 )
    """
    approved = ServiceEnrollment.objects.filter(event=event,end__gt=datetime.now(),approved=1).values('event__owner_id','user__first_name','user__last_name','team_id','team__name','start','end')
    print approved.query.__str__()
    
    #Get a list of past enrollments to review
    """
    SELECT `service_serviceenrollment`.`id`, `auth_user`.`first_name`, `auth_user`.`last_name`, 
    `service_serviceenrollment`.`team_id`, `team_team`.`name`, `service_serviceenrollment`.`start`, 
    `service_serviceenrollment`.`end` FROM `service_serviceenrollment` 
    INNER JOIN `auth_user` ON (`service_serviceenrollment`.`user_id` = `auth_user`.`id`) 
    LEFT OUTER JOIN `team_team` ON (`service_serviceenrollment`.`team_id` = `team_team`.`id`) 
    WHERE (`service_serviceenrollment`.`event_id` = 1  AND `service_serviceenrollment`.`end` < 2012-12-10 05:33:15  
    AND `service_serviceenrollment`.`approved` = 1 )
    """
    to_review = ServiceEnrollment.objects.filter(event=event,end__lt=datetime.now(),approved=1).values('id','user__first_name','user__last_name','team_id','team__name','start','end')
    print to_review.query.__str__()
    
    context = {'pending_approval':pending_approval,
               'approved':approved,
               'to_review':to_review,
    }
    if request.method == "POST":
        if "edit_event" in request.POST:
            edit_event_form = CreateEventForm(request.POST.copy(),instance=event,prefix='event')
            if edit_event_form.is_valid():
                edit_event_form.save()
                context.update({'event_update_success':True})
        else:
            edit_event_form = CreateEventForm(instance=event,prefix='event')
        if "add_skill" in request.POST:
            needs_skill_form = NeedsSkillForm(request.POST.copy(),instance=NeedsSkill(event=event),prefix='skill')
            if needs_skill_form.is_valid():
                needs_skill_form.save()
        needs_skill_form = NeedsSkillForm(prefix='skill')
    else:
        edit_event_form = CreateEventForm(instance=event,prefix='event')
        needs_skill_form = NeedsSkillForm(prefix='skill')
    #Gets the skills need by the event
    """
    SELECT `events_needsskill`.`id`, `events_needsskill`.`event_id`, `events_needsskill`.`skill_id`,
    `events_needsskill`.`min_proficiency_level` FROM `events_needsskill` WHERE `events_needsskill`.`event_id` = 1 
    """
    needed_skills = NeedsSkill.objects.filter(event=event)
    print needed_skills.query.__str__()

    context.update({'event':event,'edit_event_form':edit_event_form,
                    'needs_skill_form':needs_skill_form,
                    'needed_skills':needed_skills,
                    'proficiency':PROFICIENCY})
    return render(request,'admin_event.djhtml',context)

@event_admin
def approve_enrollment(request,event_id,enrollment_id):
    se = get_object_or_404(ServiceEnrollment,pk=enrollment_id,event_id=event_id)
    se.approved = 1
    se.save()
    return redirect("/events/{}/admin/".format(se.event_id))
