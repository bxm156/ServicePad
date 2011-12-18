from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=30)
    
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        #Verify usernames
        try:
            User.objects.get(username__exact=cleaned_data.get('email'))
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("Email already exists")
        
        #Verify Passwords
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
            del cleaned_data['password']
            del cleaned_data['confirm_password']
            
        
        return cleaned_data
    
    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['email'], self.cleaned_data['email'], self.cleaned_data.get('password'))
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.is_active = False
        new_user.save()
        return new_user