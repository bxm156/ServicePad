# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from ServicePad.apps.team.forms import NewTeamForm, InviteMember
from ServicePad.apps.team.models import Team, TeamMembership
from ServicePad.apps.service.models import ServiceRecord
from django.db.models import Sum
from ServicePad.apps.team.decorators import team_admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def create(request):
    """
    Create a team
    """
    if request.method == 'POST':
        new_data = request.POST.copy()
        team_form = NewTeamForm(new_data)
        if team_form.is_valid():
            team = Team(admin=request.user)
            new_team_form = NewTeamForm(new_data,instance=team)
            new_team = new_team_form.save()
            return redirect(new_team.get_admin_url())
        return render(request,'create_team.djhtml',{'form': team_form})
    else:
        form = NewTeamForm()
        return render(request,'create_team.djhtml',{'form': form})
    
def view(request,id):
    """
    View a team
    """
    #Get the Team
    team = get_object_or_404(Team, pk=id)
    is_admin = (request.user.id == team.admin_id)
    
    #Get the members
    """
    SELECT `auth_user`.`id`, `auth_user`.`username`, `auth_user`.`first_name`,
    `auth_user`.`last_name`, `auth_user`.`email`, `auth_user`.`password`,
    `auth_user`.`is_staff`, `auth_user`.`is_active`, `auth_user`.`is_superuser`, `auth_user`.`last_login`,
    `auth_user`.`date_joined` FROM `auth_user`
    INNER JOIN `team_teammembership` ON (`auth_user`.`id` = `team_teammembership`.`member_id`)
    WHERE (`team_teammembership`.`team_id` = 1  AND `team_teammembership`.`invite` = False )
    """
    members = team.members.filter(teammembership__invite=False)
    print members.query.__str__()

    #Get the events the team has participated in, and the total hours per event
    """
    SELECT `service_servicerecord`.`event_id`, `events_event`.`name`,
    SUM(`service_servicerecord`.`hours`) AS `hours` FROM `service_servicerecord`
    INNER JOIN `events_event` ON (`service_servicerecord`.`event_id` = `events_event`.`id`)
    WHERE (`service_servicerecord`.`attended` = True  AND `service_servicerecord`.`team_id` = 1 )
    GROUP BY `service_servicerecord`.`event_id`, `events_event`.`name` ORDER BY `hours` DESC
    """
    event_hours = ServiceRecord.objects.values('event_id').filter(team=team, attended=True).annotate(hours=Sum('hours')).order_by('-hours').values('event_id', 'event__name', 'hours')
    print event_hours.query.__str__()
    
    in_team = False
    if request.user in members:
        in_team = True
    context = {
        'team':team,
        'members':members,
        'in_team':in_team,
        'events' :event_hours,
        'is_admin' :is_admin
    }
    return render(request,'view_team.djhtml',context)
    
def list(request):
    """
    List of all teams
    """
    #Get all the Teams
    teams = Team.objects.all()
    """
    """
    print teams.query.__str__()
    return render(request,'list_teams.djhtml',
                       {'teams':teams})
    
def accept(request,team_id):
    """
    Accept a team invite
    """
    team = get_object_or_404(Team, pk=team_id)
    membership = TeamMembership.objects.get(member=request.user, team=team)
    if membership.invite == True:
        membership.invite = False
        membership.save()
    return redirect("/account/teams/")
    
def decline(request,team_id):
    """
    Decline a team invite
    """
    team = get_object_or_404(Team, pk=team_id)
    membership = TeamMembership.objects.get(member=request.user, team=team)
    membership.delete()
    return redirect("/account/teams/")

def remove (request, team_id, user_id):
    """
    Remove a member from a team
    """
    TeamMembership.objects.get(team_id = team_id, member_id = user_id).delete()
    return redirect("/teams/{}/admin/".format(team_id))
    

    
@team_admin_required
def admin(request,team_id):
    """
    Team admin page
    """
    context = {}
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        data = request.POST.copy()
        new_member_id = data.get('member',None)
        try:
            m = TeamMembership.objects.get(team=team,member_id=new_member_id)
            new_member = get_object_or_404(User,pk=new_member_id)
            if m.invite == True:
                context.update({'pending_invite':new_member.username})
            else:
                context.update({'already_member':new_member.username})
        except TeamMembership.DoesNotExist:
            membership = TeamMembership(team=team)
            invite_form = InviteMember(data,instance=membership)
            if invite_form.is_valid():
                invite_form.save()
                context.update({'invited':invite_form.cleaned_data['member']})
    #Get Members
    """
    SELECT `team_teammembership`.`member_id`, `auth_user`.`username`, `auth_user`.`first_name`, `auth_user`.`last_name`,
    `team_teammembership`.`invite` FROM `team_teammembership`
    INNER JOIN `auth_user` ON (`team_teammembership`.`member_id` = `auth_user`.`id`) WHERE `team_teammembership`.`team_id` = 2 
    """
    members = TeamMembership.objects.filter(team=team).values('member__id','member__username','member__first_name','member__last_name','invite')
    print members.query.__str__()
    
    invite_form = InviteMember() 
    context.update({
                    'team': team,
                    'invite_form': invite_form,
                    'members': members
    })
    return render(request,'admin_team.djhtml',context)
