from django import forms
from ServicePad.apps.account.models import UserProfile, Availability

class VolunteerProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('organization_name','organization_address','organization_city',
                   'organization_state','organization_postalzip','organization_phone',)
        
        
class OrganizationProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('major','graduating_class',)
        
class AvailabilityForm(forms.ModelForm):
    
    class Meta:
        model = Availability
        exclude = ('user')