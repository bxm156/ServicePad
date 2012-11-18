# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from forms import NewTeamForm
from models import Team
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

@team_admin_required
def admin(request,team_id):
    return redirect("/good/")