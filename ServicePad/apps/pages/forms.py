from django import forms
from ServicePad.apps.events.models import Skill
from ServicePad.apps.account.models import Interest

class SearchUsersForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    skill = forms.ModelChoiceField(queryset = Skill.objects.all(), required=False)
    interest = forms.ModelChoiceField(queryset = Interest.objects.all(), required=False)
