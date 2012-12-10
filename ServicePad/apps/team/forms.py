from django import forms
from models import Team, TeamMembership
from django.contrib.auth.models import User

class NewTeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        exclude = ('members','join_date','admin')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        #Verify team name is available
        try:
            Team.objects.get(name=cleaned_data.get('name'))
        except Team.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("Team name already exists")
        
        return cleaned_data
        
class InviteMember(forms.ModelForm):
    member = forms.ModelChoiceField(queryset = User.objects.filter(userprofile__account_type=0))

    class Meta:
        model = TeamMembership
        exclude = ('team','join_date','invite')