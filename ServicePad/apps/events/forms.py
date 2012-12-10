from django import forms
from models import Event
from ServicePad.apps.events.models import EventCategory, NeedsSkill, Skill
from ServicePad.apps.account.models import Interest

class CreateEventForm(forms.ModelForm):
    
    #Overide category selection to not include an empty_label option
    category = forms.ModelChoiceField(queryset = EventCategory.objects.all(), empty_label=None)

    class Meta:
        model = Event
        widgets = {
            #'start_time': JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}),
           #  'end_time': JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}),
        }
    class Media:
        css = {
               "css/ui/jquery-ui-1.8.16.custom.css",
            }
        js = (
            "js/jqsplitdatetime.js",
            "js/jquery-1.7.1.js",
            "js/jquery-ui-1.8.16.custom.min.js"
            )
class NeedsSkillForm(forms.ModelForm):
    
    class Meta:
        model = NeedsSkill
        exclude = ('event')

class SearchEventsForm(forms.Form):
    name = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset = EventCategory.objects.all(), required=False)
    skill = forms.ModelChoiceField(queryset = Skill.objects.all(), required=False)
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)
