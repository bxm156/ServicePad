from django import forms
from models import ServiceEnrollment
    
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