from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=30,required=True)
