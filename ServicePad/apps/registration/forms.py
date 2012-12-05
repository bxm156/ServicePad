from django import forms
from django.contrib.auth.models import User
from ServicePad.apps.account.models import UserProfile
import hashlib, random, datetime
from ServicePad.apps.registration.models import ActivationKey

MIN_PASSWORD_LENGTH=8
MAX_PASSWORD_LENGTH=30

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,min_length=MIN_PASSWORD_LENGTH,max_length=MAX_PASSWORD_LENGTH)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=MIN_PASSWORD_LENGTH,max_length=MAX_PASSWORD_LENGTH)
    form_type = forms.CharField(widget=forms.HiddenInput(),initial=UserProfile.ACCOUNT_VOLUNTEER)
    
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
        
        account_type = int(cleaned_data.get('form_type'))
        if account_type != UserProfile.ACCOUNT_VOLUNTEER and account_type != UserProfile.ACCOUNT_ORGANIZATION:
            raise forms.ValidationError("Invalid account type")
            
        
        return cleaned_data
    
    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['email'], self.cleaned_data['email'], self.cleaned_data.get('password'))
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.is_active = False
        new_user.save()
        
        #create the activation key
        salt = str(random.random())
        hash_salt = hashlib.sha224(salt).hexdigest()
        activation_key = hashlib.sha224(hash_salt + new_user.username).hexdigest()[:32]
        key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
        
        key_obj = ActivationKey(user=new_user,activation_key=activation_key,key_expires=key_expires)
        key_obj.save()
        
        new_profile = UserProfile(user=new_user,account_type=UserProfile.ACCOUNT_VOLUNTEER)
            
        new_profile.save()
        
        return new_user

class OrganizationRegistrationForm(forms.Form):
    business_name = forms.CharField(required=True,max_length=60)
    primary_contact_first_name = forms.CharField(required=True,max_length=30)
    primary_contact_last_name = forms.CharField(required=True,max_length=30)
    primary_contact_phone = forms.CharField(required=True,max_length=30)
    primary_contact_email = forms.EmailField(required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,min_length=MIN_PASSWORD_LENGTH,max_length=MAX_PASSWORD_LENGTH)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=MIN_PASSWORD_LENGTH,max_length=MAX_PASSWORD_LENGTH)
    form_type = forms.CharField(widget=forms.HiddenInput(),initial=UserProfile.ACCOUNT_ORGANIZATION)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        #Verify usernames
        try:
            User.objects.get(username__exact=cleaned_data.get('primary_contact_email'))
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
        new_user = User.objects.create_user(self.cleaned_data['primary_contact_email'], self.cleaned_data['primary_contact_email'], self.cleaned_data.get('password'))
        new_user.first_name = self.cleaned_data['primary_contact_first_name']
        new_user.last_name = self.cleaned_data['primary_contact_last_name']
        new_user.is_active = False
        new_user.save()
        
        salt = str(random.random())
        hash_salt = hashlib.sha224(salt).hexdigest()
        activation_key = hashlib.sha224(hash_salt + new_user.username).hexdigest()[:32]
        key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
        
        key_obj = ActivationKey(user=new_user,activation_key=activation_key,key_expires=key_expires)
        key_obj.save()

        new_profile = UserProfile(user=new_user,
                                  account_type=UserProfile.ACCOUNT_ORGANIZATION,
                                  organization_name=self.cleaned_data['business_name']
                        )
            
        new_profile.save()
        print new_profile
        
        return new_user

    