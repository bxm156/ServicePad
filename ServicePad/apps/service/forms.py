from django import forms
from models import ServiceEnrollment, ServiceRecord
    
class ServiceEnrollmentForm(forms.ModelForm):

    def clean(self):
        
        cleaned_data = super(ServiceEnrollmentForm, self).clean()
        user_start = cleaned_data.get('start')
        user_end = cleaned_data.get('end')
        
        event_start = self.instance.event.start_time
        event_end = self.instance.event.end_time

        if user_start and user_end and (user_end > event_end or user_start < event_start):
            raise forms.ValidationError("Invalid Start/End Times")
        
        return cleaned_data

    class Meta:
        model = ServiceEnrollment
        exclude = ('user','team','event','enrollment_time','approved')
        
class TeamForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        members = kwargs.pop('members')
        super(TeamForm, self).__init__(*args, **kwargs)
        
        if members:
            for user_id, name in members:
                self.fields['member_%s' % user_id] = forms.BooleanField(label=name,required=False)
            
    def get_selected_members(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('member_') and value == True:
                yield name[7:]
                
class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        exclude = ('user','team','event','hours')