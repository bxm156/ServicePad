# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from ServicePad.apps.team.forms import NewTeamForm, InviteMember
from ServicePad.apps.team.models import Team, TeamMembership
from ServicePad.apps.team.decorators import team_admin_required
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    if request.method == 'POST':
        new_data = request.POST.copy()
        team_form = NewTeamForm(new_data)
        if team_form.is_valid():
            team = Team(admin=request.user)
            new_team_form = NewTeamForm(new_data,instance=team)
            new_team = new_team_form.save()
            return redirect(new_team)
        return render(request,'create_team.djhtml',{'form': team_form})
    else:
        form = NewTeamForm()
        return render(request,'create_team.djhtml',{'form': form})
    
def view(request,id):
    team = get_object_or_404(Team, pk=id)
    members = team.members.all()
    in_team = False
    if request.user in members:
        in_team = True
    context = {
        'team':team,
        'members':members,
        'in_team':in_team
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
    
#@team_admin_required
def admin(request,team_id):
    context = {}
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        data = request.POST.copy()
        try:
            m = TeamMembership.objects.get(team=team,member=request.user)
            if m.invite == True:
                context.update({'pending_invite':request.user.username})
            else:
                context.update({'already_member':request.user.username})
        except TeamMembership.DoesNotExist:
            membership = TeamMembership(team=team)
            invite_form = InviteMember(data,instance=membership)
            if invite_form.is_valid():
                invite_form.save()
                context.update({'invited':invite_form.cleaned_data['member']})
    invite_form = InviteMember() 
    context.update({
                    'team': team,
                    'invite_form': invite_form
    })
    return render(request,'admin_team.djhtml',context)