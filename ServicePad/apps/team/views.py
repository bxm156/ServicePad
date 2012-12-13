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
    team = get_object_or_404(Team, pk=id)
    is_admin = (request.user.id == team.admin_id)
    members = team.members.filter(teammembership__invite=False)
    in_team = False
    event_hours = ServiceRecord.objects.values('event_id').filter(team=team, attended=True).annotate(hours=Sum('hours')).order_by('-hours').values('event_id', 'event__name', 'hours')
    print event_hours
    print event_hours.query.__str__()
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
    teams = Team.objects.all()
    return render(request,'list_teams.djhtml',
                       {'teams':teams})
    
def accept(request,team_id):
    team = get_object_or_404(Team, pk=team_id)
    membership = TeamMembership.objects.get(member=request.user, team=team)
    if membership.invite == True:
        membership.invite = False
        membership.save()
    return redirect("/account/teams/")
    
def decline(request,team_id):
    team = get_object_or_404(Team, pk=team_id)
    membership = TeamMembership.objects.get(member=request.user, team=team)
    membership.delete()
    return redirect("/account/teams/")

def remove (request, team_id, user_id):
    TeamMembership.objects.get(team_id = team_id, member_id = user_id).delete()
    return redirect("/teams/{}/admin/".format(team_id))
    

    
@team_admin_required
def admin(request,team_id):
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
    members = TeamMembership.objects.filter(team=team).values('member__id','member__username','member__first_name','member__last_name','invite')
    invite_form = InviteMember() 
    context.update({
                    'team': team,
                    'invite_form': invite_form,
                    'members': members
    })
    return render(request,'admin_team.djhtml',context)
