from django import forms
from django.core import validators

class RegistrationForm(forms.Form):
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=30)
    
    
    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
            del cleaned_data['password']
            del cleaned_data['confirm_password']
        return cleaned_data
    
