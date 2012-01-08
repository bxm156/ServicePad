from django import forms
from models import Event, CATEGORY_CHOICES, CATEGORY_NONE

class CreateEventForm(forms.Form):
    name = forms.CharField(required=True,max_length=30)
    short_description = forms.CharField(required=True, widget=forms.Textarea(),max_length=255)
    category1 = forms.ChoiceField(required=True, choices=CATEGORY_CHOICES)
    category2 = forms.ChoiceField(required=False,choices=CATEGORY_CHOICES)
    category3 = forms.ChoiceField(required=False,choices=CATEGORY_CHOICES)
    long_description = forms.CharField(required=True,widget=forms.Textarea())
    start_time = forms.DateTimeField(widget=forms.DateTimeInput())
    end_time = forms.DateTimeField(widget=forms.DateTimeInput())
    
    
    def clean(self):
        
        cleaned_data = self.cleaned_data
        
        category_sum = sum(
                (int(cleaned_data['category1']),
                int(cleaned_data['category2']),
                int(cleaned_data['category3'])
                ))
        if category_sum == 0:
            raise forms.ValidationError("Please select atleast 1 category")
 
        return cleaned_data
    
    def save(self,user):
        
        cleaned_data = self.cleaned_data
        new_event = Event.objects.create(event_name=cleaned_data['name'],
                         short_description=cleaned_data['short_description'],
                         long_description=cleaned_data['long_description'],
                         category=cleaned_data['category1'],
                         start_time=cleaned_data['start_time'],
                         end_time=cleaned_data['end_time'],
                         owner=user)
        return new_event
        
        