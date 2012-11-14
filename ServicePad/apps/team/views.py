# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from forms import NewTeamForm
from models import Team
def index(request):
    pass


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
    return render(request,'view_team.djhtml',
                       {'team':team})
    