from django import forms
from models import CATEGORY_CHOICES, CATEGORY_NONE

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
        pass
    
    def save(self):
        pass
        
        